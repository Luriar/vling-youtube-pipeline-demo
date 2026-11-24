# Vling 채널 정보 및 YouTube 영상 데이터 수집 파이프라인

> 이 저장소는 실제 인턴 및 별도 프로젝트 경험을 설명하기 위해 새로 작성한 공개 포트폴리오입니다. 회사의 원본 소스, 데이터베이스, 고객 정보, 운영 설정, 인증정보를 포함하지 않습니다. demo.py와 예시 데이터는 2026년에 처음부터 작성한 독립적인 오프라인 재현 예제로, 2024년 실제 운영 코드를 복제하거나 당시 배포 사실을 증명하지 않습니다.

**공개 코드 작성 시점 및 방식:** 2026년 포트폴리오 정리를 위해 AI의 도움을 받아 새로 작성한 독립 데모입니다. 2024년 당시 직접 수행한 실무 경험과 이 공개 코드의 구현 및 검증 범위는 구분합니다.

**기간:** 2024.10 별도 약 2주 프로젝트  
**실제 업무 기술:** Python, Selenium, MySQL, Flask, JSON

## 배경과 해결하려던 문제

채널 분석 데이터와 영상 성과 정보를 한 곳에서 저장하고, 이후 담당자가 조회 및 수동으로 정보를 보강할 수 있어야 했습니다.

## 직접 수행한 작업

- Vling의 채널 및 시청자 분석 데이터를 수집하여 MySQL에 저장 또는 갱신하는 기능을 구현했습니다.
- 채널 정보를 바탕으로 YouTube 영상과 Shorts 정보를 추가 수집해 영상 테이블에 저장했습니다.
- 기존 수동 입력 필드를 업데이트 중 보존하는 데이터 갱신 흐름을 구성했습니다.
- Flask 기반 채널 및 영상 조회와 수동 입력 화면 코드를 작성했습니다.

## 기여 범위 및 사실 확인

이 프로젝트는 7~9월 인턴에 포함하지 않는 10월 별도 작업입니다. 실제 서비스 사이트의 크롤링 코드, 내부 분석 데이터, 거래 정보와 운영 DB를 공개하지 않습니다. 배포 및 장기간 운영 여부는 미확인입니다.

## 공개 오프라인 데모

완전히 가상의 채널과 영상 데이터를 SQLite에 적재하고, 갱신 시 사람이 쓴 메모를 보존하는 독립 예제입니다. 네트워크 수집은 없습니다.

```bash
python demo.py
python -m unittest discover -s tests -v
```

Python 3.10 이상을 권장합니다. 외부 API 키나 실서비스 계정이 필요하지 않습니다.

## 문서

- [간단 ���계와 자료 보호](docs/ARCHITECTURE.md)
- [전체 인턴 및 프로젝트 목록](https://github.com/Luriar/dinostudio-internship-portfolio)

**주의:** 이 공개 코드는 기존 회사 프로젝트를 이전하거나 일부 수정하여 공개한 것이 아닙니다. 실제 업무 수행 내용은 설명하되 고객 데이터나 정량 성과를 공개하지 않습니다.

## 구현 보강: 데이터 적재와 정합성 검증

`pipeline.py`는 가상 채널 및 영상 데이터로 SQLite UPSERT, 외래키 검증, 배치 롤백과 수동 메모 보존을 구현했습니다. `seed.py`는 가상 JSON 데이터로 실행할 수 있습니다.

```bash
python seed.py
python -m unittest discover -s tests -v
```

이는 실제 Vling 또는 YouTube API에 접속하는 코드가 아니며, 2024년 회사 원본과 무관한 별도 구현입니다.

## 로컬 대시보드와 자동 검증

Flask 화면을 통해 가상 채널과 영상 데이터를 확인하고 별도 메모를 수정할 수 있습니다. 모든 데이터는 fixtures/sample.json에서 생성됩니다.

```bash
python -m pip install -r requirements.txt
python seed.py
python app.py
```

브라우저 주소: http://127.0.0.1:5000/

[구현 흐름과 실행 안내](docs/PIPELINE.md). GitHub Actions로 단위 테스트와 시드 적재를 자동 검증합니다.

## 재현 및 검증 범위

채널과 영상의 재적재, 수동 메모 보존, 참조 무결성과 배치 롤백, Flask 페이지 및 메모 수정 응답을 검사합니다.

2026년 공개 데모의 테스트입니다. 2024년 실무의 성능 수치나 배포 증거로 해석하지 않습니다.

- [자동 테스트 실행 이력](https://github.com/Luriar/vling-youtube-pipeline-demo/actions)
- [공개 데모 통합 검증](https://github.com/Luriar/dinostudio-internship-portfolio/blob/main/docs/INTEGRATION.md)
