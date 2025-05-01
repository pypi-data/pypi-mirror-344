
import torch
from torch import nn, optim
from tqdm import tqdm
from ..utils.evaluator import log_classification
from .loss import nt_xent_loss, importance_penalty_loss

class Trainer:
    """
    A trainer class for optimizing the Concord model.

    This class manages the training and validation of the Concord model, 
    including contrastive learning, classification, and reconstruction losses.

    Attributes:
        model (nn.Module): The neural network model being trained.
        data_structure (list): The structure of the dataset used in training.
        device (torch.device): The device on which computations are performed.
        logger (logging.Logger): Logger for recording training progress.
        use_classifier (bool): Whether to use a classification head.
        classifier_weight (float): Weighting factor for classification loss.
        unique_classes (list): List of unique class labels.
        unlabeled_class (int or None): Label representing unlabeled samples.
        use_decoder (bool): Whether to use a decoder for reconstruction loss.
        decoder_weight (float): Weighting factor for reconstruction loss.
        clr_mode (str): Contrastive learning mode ('aug' or 'nn').
        use_clr (bool): Whether contrastive learning is enabled.
        clr_weight (float): Weighting factor for contrastive loss.
        importance_penalty_weight (float): Weighting for feature importance penalty.
        importance_penalty_type (str): Type of regularization for importance penalty.

    Methods:
        forward_pass: Computes loss components and model outputs.
        train_epoch: Runs one training epoch.
        validate_epoch: Runs one validation epoch.
        _run_epoch: Handles training or validation for one epoch.
        _compute_averages: Computes average losses over an epoch.
    """
    def __init__(self, model, data_structure, device, logger, lr, schedule_ratio,
                 use_classifier=False, classifier_weight=1.0, 
                 unique_classes=None,
                 unlabeled_class=None,
                 use_decoder=True, decoder_weight=1.0, 
                 clr_mode='aug', clr_temperature=0.5, clr_weight=1.0,
                 importance_penalty_weight=0, importance_penalty_type='L1'):
        """
        Initializes the Trainer.

        Args:
            model (nn.Module): The neural network model to train.
            data_structure (list): List defining the structure of input data.
            device (torch.device): Device on which computations will run.
            logger (logging.Logger): Logger for recording training details.
            lr (float): Learning rate for the optimizer.
            schedule_ratio (float): Learning rate decay factor.
            use_classifier (bool, optional): Whether to use classification. Default is False.
            classifier_weight (float, optional): Weight for classification loss. Default is 1.0.
            unique_classes (list, optional): List of unique class labels.
            unlabeled_class (int or None, optional): Label for unlabeled data. Default is None.
            use_decoder (bool, optional): Whether to use a decoder. Default is True.
            decoder_weight (float, optional): Weight for decoder loss. Default is 1.0.
            clr_mode (str, optional): Contrastive learning mode ('aug', 'nn'). Default is 'aug'.
            clr_temperature (float, optional): Temperature for contrastive loss. Default is 0.5.
            clr_weight (float, optional): Weight for contrastive loss. Default is 1.0.
            importance_penalty_weight (float, optional): Weight for importance penalty. Default is 0.
            importance_penalty_type (str, optional): Type of penalty ('L1' or 'L2'). Default is 'L1'.
        """
        self.model = model
        self.data_structure = data_structure
        self.device = device
        self.logger = logger
        self.use_classifier = use_classifier
        self.classifier_weight = classifier_weight
        self.unique_classes = unique_classes
        self.unlabeled_class = unlabeled_class 
        self.use_decoder = use_decoder
        self.decoder_weight = decoder_weight
        self.clr_mode = clr_mode
        self.use_clr = clr_mode is not None
        self.clr_weight = clr_weight
        self.importance_penalty_weight = importance_penalty_weight
        self.importance_penalty_type = importance_penalty_type

        self.classifier_criterion = nn.CrossEntropyLoss() if use_classifier else None
        self.mse_criterion = nn.MSELoss() if use_decoder else None

        self.clr_criterion = nt_xent_loss(temperature=clr_temperature)

        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.scheduler = optim.lr_scheduler.StepLR(self.optimizer, step_size=1, gamma=schedule_ratio)

    def forward_pass(self, inputs, class_labels, domain_labels, covariate_tensors=None):
        """
        Performs a forward pass and computes loss components.

        Args:
            inputs (torch.Tensor): Input feature matrix.
            class_labels (torch.Tensor): Class labels for classification loss.
            domain_labels (torch.Tensor): Domain labels for batch normalization.
            covariate_tensors (dict, optional): Dictionary of covariate tensors.

        Returns:
            tuple: Loss components (total loss, classification loss, MSE loss, contrastive loss, importance penalty loss).
        """
        outputs = self.model(inputs, domain_labels, covariate_tensors)
        class_pred = outputs.get('class_pred')
        decoded = outputs.get('decoded')

        # Contrastive loss
        loss_clr = torch.tensor(0.0)

        if self.clr_mode == 'aug':
            outputs_aug = self.model(inputs, domain_labels, covariate_tensors)
            loss_clr = self.clr_criterion(outputs['encoded'], outputs_aug['encoded'])
            loss_clr *= self.clr_weight
        elif self.clr_mode == 'nn':
            assert inputs.size(0) % 2 == 0, "Batch size must be even for nearest neighbor contrastive loss"
            batch_size_actual = inputs.size(0) // 2
            loss_clr = self.clr_criterion(outputs['encoded'][:batch_size_actual], outputs['encoded'][batch_size_actual:])
            loss_clr *= self.clr_weight

        # Reconstruction loss
        loss_mse = self.mse_criterion(decoded, inputs) * self.decoder_weight if decoded is not None else torch.tensor(0.0)

        # Classifier loss
        loss_classifier = torch.tensor(0.0, device=self.device)
        if class_pred is not None and class_labels is not None:
            labeled_mask = (class_labels != self.unlabeled_class).to(self.device) if self.unlabeled_class is not None else torch.ones_like(class_labels, dtype=torch.bool, device=self.device)
            if labeled_mask.sum() > 0:
                class_labels = class_labels[labeled_mask]
                class_pred = class_pred[labeled_mask] 
                loss_classifier = self.classifier_criterion(class_pred, class_labels) * self.classifier_weight
            else:
                class_labels = None
                class_pred = None

        # Importance penalty loss
        if self.model.use_importance_mask:
            importance_weights = self.model.get_importance_weights()
            loss_penalty = importance_penalty_loss(importance_weights, self.importance_penalty_weight, self.importance_penalty_type)
        else:
            loss_penalty = torch.tensor(0.0)

        loss = loss_classifier + loss_mse + loss_clr + loss_penalty

        return loss, loss_classifier, loss_mse, loss_clr, loss_penalty, class_labels, class_pred

    def train_epoch(self, epoch, train_dataloader):
        """
        Runs one epoch of training.

        Args:
            epoch (int): Current epoch number.
            train_dataloader (DataLoader): Training data loader.

        Returns:
            float: Average training loss.
        """
        return self._run_epoch(epoch, train_dataloader, train=True)

    def validate_epoch(self, epoch, val_dataloader):
        """
        Runs one epoch of validation.

        Args:
            epoch (int): Current epoch number.
            val_dataloader (DataLoader): Validation data loader.

        Returns:
            float: Average validation loss.
        """
        return self._run_epoch(epoch, val_dataloader, train=False)

    def _run_epoch(self, epoch, dataloader, train=True):
        self.model.train() if train else self.model.eval()
        total_loss, total_mse, total_clr, total_classifier, total_importance_penalty = 0.0, 0.0, 0.0, 0.0, 0.0
        preds, labels = [], []

        progress_desc = f"Epoch {epoch} {'Training' if train else 'Validation'}"
        progress_bar = tqdm(dataloader, desc=progress_desc, position=0, leave=True, dynamic_ncols=True)

        for i, data in enumerate(progress_bar):
            if train:
                self.optimizer.zero_grad()

            # Unpack data based on the provided structure
            data_dict = {key: value.to(self.device) for key, value in zip(self.data_structure, data)}
            inputs = data_dict['input']
            domain_labels = data_dict.get('domain')
            class_labels = data_dict.get('class')
            covariate_keys = [key for key in data_dict.keys() if key not in ['input', 'domain', 'class', 'idx']]

            covariate_tensors = {key: data_dict[key] for key in covariate_keys}
            loss, loss_classifier, loss_mse, loss_clr, loss_penalty, class_labels, class_pred = self.forward_pass(
                inputs, class_labels, domain_labels, covariate_tensors
            )
            # Backward pass and optimization
            if train:
                loss.backward()
                self.optimizer.step()

            total_loss += loss.item()
            total_mse += loss_mse.item()
            total_classifier += loss_classifier.item() if self.use_classifier else 0
            total_clr += loss_clr.item() if self.use_clr else 0
            total_importance_penalty += loss_penalty.item() if self.model.use_importance_mask else 0

            if class_pred is not None and class_labels is not None:
                preds.extend(torch.argmax(class_pred, dim=1).cpu().numpy())
                labels.extend(class_labels.cpu().numpy())

            progress_bar.set_postfix({"loss": loss.item()})
        
        if train:
            self.scheduler.step()

        avg_loss, avg_mse, avg_clr, avg_classifier, avg_importance_penalty = self._compute_averages(
            total_loss, total_mse, total_clr, total_classifier, total_importance_penalty, len(dataloader)
        )

        self.logger.info(
            f'Epoch {epoch:3d} | {"Train" if train else "Val"} Loss:{avg_loss:5.2f}, MSE:{avg_mse:5.2f}, '
            f'CLASS:{avg_classifier:5.2f}, CONTRAST:{avg_clr:5.2f}, IMPORTANCE:{avg_importance_penalty:5.2f}'
        )
        
        if self.use_classifier:
            log_classification(epoch, "train" if train else "val", preds, labels, unique_classes=self.unique_classes, logger=self.logger)

        return avg_loss


    def _compute_averages(self, total_loss, total_mse, total_clr, total_classifier, total_importance_penalty, dataloader_len):
        avg_loss = total_loss / dataloader_len
        avg_mse = total_mse / dataloader_len
        avg_clr = total_clr / dataloader_len
        avg_classifier = total_classifier / dataloader_len
        avg_importance_penalty = total_importance_penalty / dataloader_len
        return avg_loss, avg_mse, avg_clr, avg_classifier, avg_importance_penalty
    