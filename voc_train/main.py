'''
TODO
check whether iou, pix acc is not wrong to control the voc data.
'''

from train import train
from fcn import FCN18
from utils import label_accuracy_score

import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

if __name__ == '__main__': 
  if torch.cuda.is_available():
    device = torch.device('cuda')
    torch.cuda.manual_seed_all(1)
  else:
    device = torch.device('cpu')
    torch.manual_seed(1)
  print(torch.__version__, device)

  model = FCN18(21, device).to(device)
  PATH = 'voc_train/fcn_model/model_96_2111_90'
  checkpoint = torch.load(PATH)
  model.load_state_dict(checkpoint['model_state_dict'])
  
  lr = 1e-3
  weight_decay = 1e-4
  momentum = 0.9
  
  optimizer = optim.SGD(model.parameters(), lr=lr, momentum=momentum, weight_decay=weight_decay)
  criterion = nn.CrossEntropyLoss(ignore_index=-1).to(device)
  scheduler = optim.lr_scheduler.MultiStepLR(optimizer, milestones=[50,250], gamma=0.1)
  # scheduler = None

  # train
  history = train(model, optimizer, criterion, scheduler, epochs = 300, \
                  device=device, verbos_iter=False)
  plt.plot(history)
  plt.show()
  
  # seg_plot(model, 0, device=device)
  # mean_iou(model, device=device, verbose=False)
  # mean_foreground_pixel_acc(model, device=device, verbose=False)
  acc, acc_cls, mean_iu, fwavacc = label_accuracy_score(model, 21, device=device, verbose=True)