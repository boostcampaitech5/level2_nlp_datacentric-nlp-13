from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report


'''
classification report
'''
def classification_report(y_true, y_predicted):
    report = classification_report(y_true, y_predicted)
    print(report)



'''
confusion matrix
'''

def confusion_matrix(y_true, y_predicted, norm=True):
    if norm = True:
        confusion_matrix  = confusion_matrix.astype('float') / confusion_matrix.sum(axis=1)[:, np.newaxis]
    else:
        confusion_matrix = confusion_matrix(y_true, y_predicted)
    
    # 클래스 레이블
    labels=['IT/Science', 'Economy','Social','Life&Culture','World','Sports', 'Politics']

    fig, ax = plt.subplots()
    sns.heatmap(confusion_matrix, annot=True,fmt = 'd', cmap='Blues', xticklabels=labels, yticklabels=labels)
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    ax.set_title('Confusion Matrix')
    plt.show()
