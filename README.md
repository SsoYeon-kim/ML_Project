4학년 머신러닝 중 프로젝트      

## 1. 문제   

**군집의 중심 각도를 추정하는 NN 만들기**

-----train_data.npy-----
* 각 데이터는 100개의 복소수로 구성
* 20000 × 100 array   
* 20000개 데이터, 각 데이터는 100개의 복소수
* 각 데이터는 동일한 위상에 노이즈가 섞인 것
   
-----target_data.npy-----   
* 20000개의 복소수의 위상 값
* 20000 × 1 array
* 각 범위는 0~2π    
   
-----성능 평가지표------   
* 학습 mse, Test Data에 mse   
* Average((target위상 - 추정한 위상)^2)   
* 입력 노드의 개수는 자유롭게 구성, Layer 수도 자유롭게   
   
## 2. 실패 사례   
   
데이터의 0,1,2를 꺼내 산점도를 그려보았을 때 데이터 상관성이 없는 모양으로 선형회귀는 쓸 수 없다 생각했지만 train_data에서 허수를 빼주었을 때 데이터 상관성이 있는 모양으로 선형 회귀를 사용할 수 있을 것이라 생각했다.   
   
<img src = "https://user-images.githubusercontent.com/62587484/147489495-5d8ad095-b574-4825-b99f-7aeb6496f940.jpg" width = 60%> 
   
하지만 이를 농어 길이,무게 데이터의 산점도와 비교해 보았을 때 비슷한 위상을 갖긴 하지만 노이즈가 섞여 상대적으로 둥근 모양이며 학습 후 정확도를 고려해보았을 때 선형회귀는 적합하지 않다고 생각했다.    
   
<img src = "https://user-images.githubusercontent.com/62587484/147489641-4cfd40dd-baea-447c-94d7-6c85cfc440e5.jpg" width = 60%> 
   
따라서 DNN을 사용하였다.   
   
## 3. 입력 가공   
   
20000 × 100 array인 입력 데이터를 실수와 허수로 나누어 준 후 이를 1 × 2000000 array로 만들어 주었다. 그 후 column_stack을 이용해 아래와 같은 2000000 × 2 array으로 바꾼 후 실수와 허수가 번갈아가도록 펼쳐준 후 reshape을 통해 3차원으로 만들어 주었다.    
   
<img src = "https://user-images.githubusercontent.com/62587484/147488942-494958ef-d190-44b2-b6e3-e062f381c947.jpg" width = 50%><img src = "https://user-images.githubusercontent.com/62587484/147489078-8f03da65-1bd3-4045-afbd-68af13bf2398.jpg" width = 50%> 
     
따라서 데이터의 첫 번째를 비교해보았을 때 j를 제외하고 실수와 허수가 번갈아가며 존재하는 입력데이터를 사용했다.  
   
<img src = "https://user-images.githubusercontent.com/62587484/147489110-5f2ca100-b819-49e9-939e-1b52233c3741.jpg" width = 60%>  
   
## 4. 문제 해결 과정   
   
 Layer층 개수, 노드 수 등에 대한 여러가지 실험을 해봤지만 노드와 층 수가 늘어난다고해서 성능이 향상된다고 느끼지 못했다.   
    
<img src = "https://user-images.githubusercontent.com/62587484/147489986-dd3db55f-4cd0-4a67-80b2-a2bf95984c97.jpg" width = 60%> 
   
따라서 아래와 같은 모델의 구조를 만들었다. 오른쪽 사진은 epoch 1000을 돌렸을 때 그래프이다.   
   
<img src = "https://user-images.githubusercontent.com/62587484/147490111-4706e2a4-31d2-4f14-8b90-c5a23377ed52.jpg" width = 60%> 
    
시간이 지남에 따라 성능이 향상하지 않아 조기 종료 조건을 추가하였으며 최종적으로 3개의 Layer층, 노드 수는 순서대로 100,220,300으로 지정하였다. Dropout은 0.2로 설정하였으며 Optimizer는 adam, Activation function은 위상 값이 0~2π를 가지므로 relu를 사용했다.   
   
<img src = "https://user-images.githubusercontent.com/62587484/147490186-89a27084-cd9f-4ad9-b969-2015d2a5a66e.jpg" width = 60%> 
    
## 5. 학습 결과   
   
실행할 때마다 차이가 나타나지만 결과가 잘 나올 때는 테스트 세트의 평균 제곱 오차가 0.09까지 내려갔다. 오른쪽 그래프는 오차의 분포를 나탄는 그래프이다.    
   
<img src = "https://user-images.githubusercontent.com/62587484/147490347-2221ddfb-1aa7-4ff5-b286-83c53359025e.jpg" width = 60%> 
    
## 6. 그 밖에 필요하다고 생각하는 내용   
   
여러번 실행을 해보면서 테스트 데이터가 진동한 적이 많았다. 따라서 Learning rate를 0.001을 기준으로 낮추거나 올려보았을 때 아래와 같은 결과가 나왔다.   
   
<img src = "https://user-images.githubusercontent.com/62587484/147490451-2f5721c5-2599-405e-9a04-d23f0f06b3c5.jpg" width = 60%> 
   
Learning rate를 낮췄을 때 테스트 데이터의 진동이 훨씬 적었지만 학습 시간과 수렴의 문제가 있을 수 있으므로 여러 번 실험을 통해 적당한 값을 지정해줘야 될 것 같다.
