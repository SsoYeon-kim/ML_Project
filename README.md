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
   
<img src = "https://user-images.githubusercontent.com/62587484/147489495-5d8ad095-b574-4825-b99f-7aeb6496f940.jpg" width = 50%> 
   
하지만 이를 농어 길이,무게 데이터의 산점도와 비교해 보았을 때 비슷한 위상을 갖긴 하지만 노이즈가 섞여 상대적으로 둥근 모양이며 학습 후 정확도를 고려해보았을 때 선형회귀는 적합하지 않다고 생각했다.    
   
<img src = "https://user-images.githubusercontent.com/62587484/147489641-4cfd40dd-baea-447c-94d7-6c85cfc440e5.jpg" width = 50%> 
   
따라서 DNN을 사용하였다.   
   
## 3. 입력 가공   
   
20000 × 100 array인 입력 데이터를 실수와 허수로 나누어 준 후 이를 1 × 2000000 array로 만들어 주었다. 그 후 column_stack을 이용해 아래와 같은 2000000 × 2 array으로 바꾼 후 실수와 허수가 번갈아가도록 펼쳐준 후 reshape을 통해 3차원으로 만들어 주었다. 
<img src = "https://user-images.githubusercontent.com/62587484/147488942-494958ef-d190-44b2-b6e3-e062f381c947.jpg" width = 50%><img src = "https://user-images.githubusercontent.com/62587484/147489078-8f03da65-1bd3-4045-afbd-68af13bf2398.jpg" width = 50%> 
     
따라서 데이터의 첫 번째를 비교해보았을 때 j를 제외하고 실수와 허수가 번갈아가며 존재하는 입력데이터를 사용했다.   
<img src = "https://user-images.githubusercontent.com/62587484/147489110-5f2ca100-b819-49e9-939e-1b52233c3741.jpg" width = 50%>  
