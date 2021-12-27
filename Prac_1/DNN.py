import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow import keras

train_data = np.load('train_data.npy')  #(20000,100)
target_data = np.load('train_target.npy')   #(20000,1)

t_real = train_data.real  #(20000,100)
t_img = train_data.imag   #(20000,100)

real = t_real.reshape(-1,)  #(2000000,)
img = t_img.reshape(-1,)    #(2000000,)

cs_input = np.column_stack((real,img)) #(2000000,2)
input = cs_input.reshape(-1,)   #(4000000,)

#20000개 데이터 1행 200열 (100개의 복소수 데이터 -> 실,허,실,허 ... ==>200열)
#입력 데이터
input_data = input.reshape(20000,1,200)
#print(input_data[0])  #(1, 200)

train_input, val_input, train_target, val_target = train_test_split(
    input_data, target_data, test_size=0.2, random_state=42)


def model_fn(a_layer=None):
    model = keras.Sequential()
    #input 노드
    model.add(keras.layers.Flatten(input_shape=(1, 200)))

    #hidden layer
    model.add(keras.layers.Dense(100, activation='relu'))
    model.add(keras.layers.Dense(220, activation='relu'))
    model.add(keras.layers.Dense(300, activation='relu'))

    if a_layer:
        model.add(a_layer)

    #output 노드
    model.add(keras.layers.Dense(1, activation='relu'))
    return model

model = model_fn(keras.layers.Dropout(0.2))
#model.summary()

model.compile(optimizer='adam',
              loss='mse', metrics=['mse'])

checkpoint_cb = keras.callbacks.ModelCheckpoint('best-simplednn-model.h5')
early_stopping_cb = keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True)

history = model.fit(train_input, train_target, epochs=1000,
                    validation_data=(val_input, val_target),
                    callbacks=[checkpoint_cb, early_stopping_cb])

print("----------------------------------------------")

# loss, mse = model.evaluate(val_input, val_target)
# print("테스트 세트의 평균 제곱 오차 : {:5.2f}".format(mse))

plt.plot(history.history['loss'], label='Train Error')
plt.plot(history.history['val_loss'], label='Val Error')
plt.xlabel('epoch')
plt.ylabel('mse')
plt.legend()
plt.show()

prediction = model.predict(val_input)
plt.scatter(val_target, prediction)
plt.xlabel("True Values")
plt.ylabel("Predictions")
plt.show()

error = prediction - val_target
plt.hist(error, bins=25)
plt.xlabel("Prediction Error")
_ = plt.ylabel("Count")
plt.show()

#모델 그림
# keras.utils.plot_model(model)
# keras.utils.plot_model(model, show_shapes=True, to_file='dnn-architecture.png', dpi=300)
