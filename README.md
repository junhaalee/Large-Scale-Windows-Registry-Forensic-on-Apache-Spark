# Large-Scale Windows Registry Forensic on Apache Spark - 아파치 스파크를 이용한 대용량 윈도우 레지스트리 데이터 포렌식 분석

## 프로젝트 소개

대용량의 윈도우 레지스트리 데이터를 HDFS 상에 저장하고, 윈도우 상에서 레지스트리 데이터를 다루는 다양한 자체 API들을 Apache Spark를 통해 구현함으로써 분산 데이터베이스 환경에서 윈도우 레지스 트리에 대한 처리가 가능함을 보이고, Spark를 통해 구현한 다양한 함수들의 조합을 통해 윈도우 레지스트리에 대한 포렌식 분석 방법을 제안.


## Contents

- [Material](https://github.com/junhaalee/registry_Forensic/tree/master/Material)
	- 논문 구성 자료

- [Code](https://github.com/junhaalee/registry_Forensic/tree/master/code)
	
	- [Experiment - Partition 개수 및 Node 개수를 다르게 설정한 Operation](https://github.com/junhaalee/registry_Forensic/tree/master/code/Experiment)
		- Registry Key를 이용한 Search
		- Keyword를 이용한 Search
		- 전체 레지스트리를 비교하는 Forensic

	- [Operations](https://github.com/junhaalee/registry_Forensic/tree/master/code/Operations)
		- Reg2Json : 윈도우 레지스트리에서 export된 reg 파일을 json 형식의 dictionary 파일로 바꾸는 과정
		
		- Registry_Operation : 윈도우 레지스트리 전용 API(ex. RegOpenKey, RegQueryKey 등)를 Python을 통해 구현
		
		- Registry_Operation_pyspark : 분산환경에서 윈도우 레지스트리 데이터를 전처리하는 Operation 및 윈도우 레지스트리 전용 API(ex. RegOpenKey, RegQueryKey 등)를 PySpark를 통해 구현.
				
			- reg2dict() : 윈도우 레지스트리에서 export된 reg 파일의 line 별로 Registry Key와 Registry Value를 식별하여 key-value data 생성
		
			- dictReduce() : regdict()에서 생성된 여러 개의 key-value data를 공통되는 key 별로 value들을 병합하여 하나의 Tree 구조의 Data로 변환

		- forensic_pyspark : 분산환경에서 둘 이상의 전체 레지스트리 파일을 비교.

	- [Setting - GCP에서 실험을 진행하기 위한 Setting 파일](https://github.com/junhaalee/registry_Forensic/tree/master/code/Setting)

