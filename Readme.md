Kovid Mail
===
***
Kovid Mail은 대한민국 코로나 19 바이러스 일일 현황을 아침 10~11시에 메일로 보내주는 서비스 입니다. 메일 내용으로는 일일 현황, 최근 4일간의 데이터 그래프(전체 확진자 수, 금일 확진자 수),세가지 주제에 대한 뉴스를 포함하고 있습니다.
***
각 버전에 대한 설명은 [Release](https://github.com/J-hoplin1/KovidMail/releases)를 참고해주시면 감사하겠습니다.
***
### Required Spec

- Python 3.8 or upper

- RDBMS : Maria DB or MySQL

### How I operate service now(Standard : 2021 / 12 / 16)

- Synology NAS / Docker - Ubuntu Image(LTS)

- Synology NAS / Maria DB - External Access

- RAM Usage Benchmark
  - manage.py : 65mb ~ 70mb
  - app.py : 100mb ~ 120mb
***
### Basic Manuals
![image](https://user-images.githubusercontent.com/45956041/146395663-369bdd36-3fa2-4006-ab85-03cc0786f01f.png)

scheduler 혹은 app을 처음실행하면 보게될 화면입니다. 이 부분에서는 자신이 연결할 데이터 베이스 정보를 입력해 주면 됩니다. 만약 외부 SQL서버에 연결한다면 외부 IP혹은 도메인을 입력해주세요. 입력이 완료된 후 해당 정보로 연결을 할 수 없는경우, 다시 입력하도록 창이 뜹니다. 이 화면은 데이터 베이스 연결을 시도할때 실패하는 경우 항상 뜨게 됩니다.

![image](https://user-images.githubusercontent.com/45956041/146395754-649a01e0-edbe-4534-9278-008518428464.png)

이 화면은 서비스에 있어 기본적으로 필요한 키값, SMTP Auth정보를 입력하는 부분입니다. 기본적으로 이 애플리케이션에서는 Naver SMTP를 사용하는거로 되어있습니다. 사용하기 위해서는 사용할 계정의 SMTP설정을 해주시기 바랍니다. 각 필드별로 어떤 API로 부터 키값을 가져와야하는지 적어두겠습니다.

  - OPENAPIURL , OPENAPIKey : https://www.data.go.kr/iim/api/selectAPIAcountView.do | API Key는 Decoding버전을 입력해 주셔야 합니다.
  - NAVERREQURL,NAVERID,NAVERKEY : https://developers.naver.com/docs/serviceapi/search/news/news.md#%EB%89%B4%EC%8A%A4 | NAVERREQURL은 JSON을 response하는 URL로 입력해주세요
  - HOSTERMAIL,HOSTERMAILPW : 자신이 메일 보내는데 사용할 네이버 메일주소(???@naver.com)과 비밀번호를 입력해주세요. 비밀번호는 보안을 위해 2차보안을 하여 비밀번호를 따로 발급받아 입력하시는것을 추천드립니다.

![image](https://user-images.githubusercontent.com/45956041/146397323-ab6e8066-e18c-4e16-a121-f9b3a180f017.png)

Manage Tool 메인 화면입니다. 각 옵션의 숫자를 입력하여주시면 됩니다.

![image](https://user-images.githubusercontent.com/45956041/146397541-396702e8-a6b9-4a26-aa83-e5c7b75ad81c.png)
![image](https://user-images.githubusercontent.com/45956041/146397918-8e39ad3d-220a-427d-b794-bb8f6eccabe2.png)


Manage Tool메인화면에서 6번을 입력하면 Config Writer로 들어올 수 있습니다. Config Writer는 SQL에 연결하기 위한 데이터를 관리하는 config.yml에 대한 인터페이스 입니다. Config Writer에서 모든 옵션에는 비밀번호를 입력해야합니다. 초기 비밀번호는 'admin'이며, 4 Change_config_pw를 통해서 바꿔주실 수 있습니다. Config Writer에서 설정값 변경 후 종료시 SQL에 다시 연결합니다. 만약 바뀐 데이터로 연결할 수 없다면, 설정값을 다시 입력하는 창으로 가게 됩니다

![image](https://user-images.githubusercontent.com/45956041/146398070-03ec7244-7819-43ca-a87f-5511156dd738.png)
![image](https://user-images.githubusercontent.com/45956041/146398528-15ebb6c6-526b-4e4c-ba56-45dfd2e987c7.png)
![image](https://user-images.githubusercontent.com/45956041/146398629-51f63c00-2416-4a4d-a1ee-8fcfe10c69bd.png)

Database Manger입니다 Manage Tool에서 7번을 입력하면 Database Manager로 들어올 수 있습니다. 두번째 사진이 Reset을 한 후 입니다. Reset_Database를 한 후에 exit을 하면 서비스가 잠기면서 키값들을 입력하는창으로 가게 됩니다.

이 이상 자세한 메뉴얼은 추후 업데이트 하도록 하겠습니다
***
### Work Stream Chart

![image](https://user-images.githubusercontent.com/45956041/146683952-9d04dcde-1eb2-4411-af8e-5016cfed0a61.png)





