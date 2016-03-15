# twitter_import_toes
For NCCU Floodfire Team, let twitter data import to elasticsearch.

## 資料來源及格式
負責 twitter 撈資料的小組所存成的資料。 
輸入的資料格式為 .xlsx

(可參考 twitter_source.xlsx 格式)

---
## 使用方法
python 3 環境，command line 下
```
$ python twitter_import_es.py oooo.xlsx
```
用 python 執行 twitter_import_es.py, 給的資料檔案為 oooo.xlsx 

#### 回傳結果
The filename is **檔案名稱.xlsx**.
The situation of importing data (the first site is count number): ** (資料進去筆數, 錯誤訊息) **


---

#### 附註
* 會自動產生一個 csv 檔 ，可參考 twitter_data.csv
* 若有遇到 編碼問題，如：`UnicodeDecodeError: 'ascii' codec can't decode byte 0xec in position 101: ordinal not in range(128)`
建議可以在確定是否在 py3 環境
* 如想看到此 index 的 schema，可將 print (es_index.get_mapping(index=indexName,doc_type=typeName)) 給打開（即消去 # )
