class Libraries:
    text = '''
import pandas as pd
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
'''

    def __str__(self):
        return self.text

class Code:
    text = '''
df = pd.read_csv(r"Bank_Loan.csv")
df = df.drop(columns=['ZIP Code'])
df.head()


x = df.drop(columns=['Personal Loan'])
y = df['Personal Loan']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)


x_train = torch.tensor(x_train, dtype=torch.float32)
x_test = torch.tensor(x_test, dtype=torch.float32)
y_train = torch.tensor(y_train.values, dtype=torch.float32).view(-1, 1)
y_test = torch.tensor(y_test.values, dtype=torch.float32).view(-1, 1)



class LoanDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


train_dataset = LoanDataset(x_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

'''

    def __str__(self):
        return self.text


class Swish:
    text = '''
# Swish activation function
class Swish(nn.Module):
    def forward(self, x):
        return x * torch.sigmoid(x)
      
      
        
class LoanModel(nn.Module):
    def __init__(self):
        super(LoanModel, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(x_train.shape[1], 16),  
            Swish(),                          
            nn.Linear(16, 8),                 
            Swish(),                          
            nn.Linear(8, 1),                  
            nn.Sigmoid()                      
        )

    def forward(self, x):
        return self.net(x)
        
        
        
model = LoanModel()
criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)



loss_values = []
accuracy_values = []

for epoch in range(50):
    model.train()
    epoch_loss = 0

    # Iterate through each batch
    for batch_X, batch_y in train_loader:
        outputs = model(batch_X)           
        loss = criterion(outputs, batch_y) 

        optimizer.zero_grad()  
        loss.backward()        
        optimizer.step()       

        epoch_loss += loss.item() 

    avg_loss = epoch_loss / len(train_loader)
    loss_values.append(avg_loss)

    model.eval()
    with torch.no_grad():
        val_preds = model(x_test)
        val_predicted = (val_preds > 0.5).float() 
        val_accuracy = (val_predicted == y_test).sum() / y_test.shape[0]
        accuracy_values.append(val_accuracy.item()) 

    print(f'Epoch {epoch}, Loss: {avg_loss:.4f}, Accuracy: {val_accuracy.item():.4f}')
    
    
    
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(loss_values, label='Training Loss', color='blue')
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Loss Curve - Swish Activation")
plt.grid(True)
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(accuracy_values, label='Validation Accuracy', color='green')
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.title("Accuracy Curve - Swish Activation")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()



with torch.no_grad():
    preds = model(x_test)                  
    predicted = (preds > 0.5).float()         
    accuracy = (predicted == y_test).sum() / y_test.shape[0]  
    print(f'\nFinal Test Accuracy: {accuracy.item():.4f}')



cm = confusion_matrix(y_test.numpy().astype(int), predicted.numpy().astype(int))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["No Loan", "Loan"])
disp.plot(cmap='Blues')
plt.title("Confusion Matrix - Swish Activation")
plt.show()

    '''
    def __str__(self):
        return self.text


class ReLU:
    text = '''
# ReLU
class LoanModel(nn.Module):
    def __init__(self):
        super(LoanModel, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(x_train.shape[1], 16),
            nn.ReLU(),             
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 1),
            nn.Sigmoid()            
        )

    def forward(self, x):
        return self.net(x)



model = LoanModel()
criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)


loss_values = []
accuracy_values = []

for epoch in range(50):
    model.train()
    epoch_loss = 0

    # Iterate through each batch
    for batch_X, batch_y in train_loader:
        outputs = model(batch_X)           
        loss = criterion(outputs, batch_y) 

        optimizer.zero_grad()  
        loss.backward()        
        optimizer.step()       

        epoch_loss += loss.item() 

    avg_loss = epoch_loss / len(train_loader)
    loss_values.append(avg_loss)

    model.eval()
    with torch.no_grad():
        val_preds = model(x_test)
        val_predicted = (val_preds > 0.5).float() 
        val_accuracy = (val_predicted == y_test).sum() / y_test.shape[0]
        accuracy_values.append(val_accuracy.item()) 

    print(f'Epoch {epoch}, Loss: {avg_loss:.4f}, Accuracy: {val_accuracy.item():.4f}')
    
    
    
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(loss_values, label='Training Loss', color='blue')
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Loss Curve - ReLU Activation")
plt.grid(True)
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(accuracy_values, label='Validation Accuracy', color='green')
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.title("Accuracy Curve - ReLU Activation")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()



with torch.no_grad():
    preds = model(x_test)                  
    predicted = (preds > 0.5).float()         
    accuracy = (predicted == y_test).sum() / y_test.shape[0]  
    print(f'\nFinal Test Accuracy: {accuracy.item():.4f}')
    
    
    
cm = confusion_matrix(y_test.numpy().astype(int), predicted.numpy().astype(int))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["No Loan", "Loan"])
disp.plot(cmap='Blues')
plt.title("Confusion Matrix - ReLU Activation")
plt.show()

    '''
    def __str__(self):
        return self.text
    
    
class Tanh:
    text = '''
# Tanh
class LoanModel(nn.Module):
    def __init__(self):
        super(LoanModel, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(x_train.shape[1], 16),
            nn.Tanh(),
            nn.Linear(16, 8),
            nn.Tanh(),
            nn.Linear(8, 1),
            nn.Sigmoid() 
        )

    def forward(self, x):
        return self.net(x)
        
        
        
model = LoanModel()
criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    
   
    
loss_values = []
accuracy_values = []

for epoch in range(50):
    model.train()
    epoch_loss = 0

    # Iterate through each batch
    for batch_X, batch_y in train_loader:
        outputs = model(batch_X)           
        loss = criterion(outputs, batch_y) 

        optimizer.zero_grad()  
        loss.backward()        
        optimizer.step()       

        epoch_loss += loss.item() 

    avg_loss = epoch_loss / len(train_loader)
    loss_values.append(avg_loss)

    model.eval()
    with torch.no_grad():
        val_preds = model(x_test)
        val_predicted = (val_preds > 0.5).float() 
        val_accuracy = (val_predicted == y_test).sum() / y_test.shape[0]
        accuracy_values.append(val_accuracy.item()) 

    print(f'Epoch {epoch}, Loss: {avg_loss:.4f}, Accuracy: {val_accuracy.item():.4f}')
    



plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(loss_values, label='Training Loss', color='blue')
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Loss Curve - Tanh Activation")
plt.grid(True)
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(accuracy_values, label='Validation Accuracy', color='green')
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.title("Accuracy Curve - Tanh Activation")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()



with torch.no_grad():
    preds = model(x_test)                  
    predicted = (preds > 0.5).float()         
    accuracy = (predicted == y_test).sum() / y_test.shape[0]  
    print(f'\nFinal Test Accuracy: {accuracy.item():.4f}')
    
    
cm = confusion_matrix(y_test.numpy().astype(int), predicted.numpy().astype(int))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["No Loan", "Loan"])
disp.plot(cmap='Blues')
plt.title("Confusion Matrix - Tanh Activation")
plt.show()
    '''
    def __str__(self):
        return self.text
    
class LeakyReLU:
    text = '''
# LeakyReLU
class LoanModel(nn.Module):
    def __init__(self):
        super(LoanModel, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(x_train.shape[1], 16),
            nn.LeakyReLU(negative_slope=0.01),
            nn.Linear(16, 8),
            nn.LeakyReLU(negative_slope=0.01),
            nn.Linear(8, 1),
            nn.Sigmoid()
        )
        
    def forward(self, x):
        return self.net(x)    



model = LoanModel()
criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)



loss_values = []
accuracy_values = []

for epoch in range(50):
    model.train()
    epoch_loss = 0

    # Iterate through each batch
    for batch_X, batch_y in train_loader:
        outputs = model(batch_X)           
        loss = criterion(outputs, batch_y) 

        optimizer.zero_grad()  
        loss.backward()        
        optimizer.step()       

        epoch_loss += loss.item() 

    avg_loss = epoch_loss / len(train_loader)
    loss_values.append(avg_loss)

    model.eval()
    with torch.no_grad():
        val_preds = model(x_test)
        val_predicted = (val_preds > 0.5).float() 
        val_accuracy = (val_predicted == y_test).sum() / y_test.shape[0]
        accuracy_values.append(val_accuracy.item()) 

    print(f'Epoch {epoch}, Loss: {avg_loss:.4f}, Accuracy: {val_accuracy.item():.4f}')
    
    

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(loss_values, label='Training Loss', color='blue')
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Loss Curve - LeakyReLu Activation")
plt.grid(True)
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(accuracy_values, label='Validation Accuracy', color='green')
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.title("Accuracy Curve - LeakyReLu Activation")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()



with torch.no_grad():
    preds = model(x_test)                  
    predicted = (preds > 0.5).float()         
    accuracy = (predicted == y_test).sum() / y_test.shape[0]  
    print(f'\nFinal Test Accuracy: {accuracy.item():.4f}')
    
    
    
cm = confusion_matrix(y_test.numpy().astype(int), predicted.numpy().astype(int))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["No Loan", "Loan"])
disp.plot(cmap='Blues')
plt.title("Confusion Matrix - LeakyReLu Activation")
plt.show()
    '''
    def __str__(self):
        return self.text
    
    
class SoftMax:
    text = '''
# Softmax
y = df['Personal Loan']



y_train = y_train.long()
y_test = y_test.long()



def __getitem__(self, idx):
    return self.X[idx], self.y[idx]
    
    
    
class LoanModel(nn.Module):
    def __init__(self):
        super(LoanModel, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(x_train.shape[1], 16),
            nn.ReLU(),               # or Swish/Tanh/LeakyReLU
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 3),         
            nn.Softmax(dim=1)        
        )

    def forward(self, x):
        return self.net(x)



model = LoanModel()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)



val_preds = model(x_test)
val_predicted = torch.argmax(val_preds, dim=1)
val_accuracy = (val_predicted == y_test).sum() / y_test.shape[0]



cm = confusion_matrix(y_test.numpy(), val_predicted.numpy())
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["No Loan", "Loan"])
disp.plot(cmap='Blues')
plt.title("Confusion Matrix - SoftMax Activation")
plt.show()
    '''
    def __str__(self):
        return self.text