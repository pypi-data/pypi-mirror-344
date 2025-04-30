# PreKO: Precise KO system
Analysis pipeline for PreKO project


### InDelSearcher: Cas9 nuclease indel analyzer
InDelSearcher는 target sequence에서 indel frequency를 분석하고 계산해주는 파이프라인이다. 특히, high-throughput screening 데이터에서 barcode에 따른 indel frequency를 분석하는 것에 특화되어 있다. 

분석을 위해서, 아래와 같이 barcode와 target sequence 정보가 담긴 csv 파일이 필요하다. 


| Barcode             | Target_region               | Reference_sequence                                            |
| ------------------- | --------------------------- | ------------------------------------------------------------- |
| TTTGCTGTGAGCACTGCTG | TTGTGAACATAGATCCATTTTTCTTGG | CTTGAAAAAGTGGCACCGAGTCGGTGCTTTTTTNNNNNNNNTTTGCTGTGAGCACTGCTGT |
| TTTGGACGTCATAGTGAGA | TCCAGATAGTCATCAACTTTTTGTTGG | CTTGAAAAAGTGGCACCGAGTCGGTGCTTTTTTNNNNNNNNTTTGGACGTCATAGTGAGAT |
| TTTGGCTATCTGCACGTGC | GTGGGGGGCCTGGGGCCTGGAGCCTGG | CTTGAAAAAGTGGCACCGAGTCGGTGCTTTTTTNNNNNNNNTTTGGCTATCTGCACGTGCG |
| TTTGATGCGCATCTCTACG | CCCAGGCAAAACTGCAGTTTTACCTGG | CTTGAAAAAGTGGCACCGAGTCGGTGCTTTTTTNNNNNNNNTTTGATGCGCATCTCTACGC |
| TTTGACTCGAGTCTCTCAC | ACGAGGTGGCCCTGGGGGGCCCCCTGG | CTTGAAAAAGTGGCACCGAGTCGGTGCTTTTTTNNNNNNNNTTTGACTCGAGTCTCTCACA |


barcode 파일과 분석할 FASTQ 파일이 있다면, InDelSearcher를 이용한 분석을 할 수 있다. 

```python
import pandas as pd
from PreKO.indel import InDelSearcher

# Setting: required information
DIR_FASTQ   = f'NGS_data/Cas9_FASTQ_combined/'
barcode     = f'ref_Small_Cas9_KO_Lib.csv'

sample_name = f'HCT_Cas9_R1_Day7'
fastq_file  = f'{DIR_FASTQ}/{sample_name}.fastq'

ids = InDelSearcher()

# Run and show summary
df_summary = ids.run(strFq=fastq_file, barcode=barcode, sample_name=sample_name, thread=25)
df_summary.to_csv(f'InDel_Summary_{sample_name}.csv')
```


# Environments
These codes were tested in Ubuntu 22.04 LTS environments.

# Requirements
- Python >= 3.8
- biopython
- pandas
- numpy
- pydantic
- tqdm