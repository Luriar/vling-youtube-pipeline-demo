# 공개용 Vling 및 YouTube 데이터 처리 예제

2024년 별도 프로젝트 경험을 설명하기 위해 2026년 독립적으로 구현한 가상 파이프라인입니다. 실제 Vling / YouTube 접속과 회사 원본 코드 재사용은 하지 않습니다.

흐름: 가상 채널 JSON → 유효성 및 외래키 검사 → SQLite 채널 UPSERT → 가상 영상 JSON → 영상 UPSERT → Flask 조회와 메모 관리.

## 실행 방법

1. python -m pip install -r requirements.txt
2. python seed.py
3. python app.py
4. http://127.0.0.1:5000/ 로 접속

가상 채널과 영상 표를 조회하고 메모를 수정할 수 있습니다. API는 /api/channels, /api/videos, /api/summary 입니다.

## 안정성

- SQLite 트랜잭션으로 잘못된 배치가 전부 롤백됩니다.
- 갱신 시 수동 메모는 보존됩니다.
- 모든 데이터는 fixtures/sample.json 안의 가상 레코드입니다.
- 서버는 오직 127.0.0.1에 바인딩되며 공개 배포 용도가 아닙니다.
- 과거 실제 채널 수집량과 2026년 데모 수집량을 혼동하지 않습니다.
