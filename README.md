
create env
```bash
conda create -n wineq python==3.7 -y
```

activate env
```bash
conda activate wineq
```

create a requirement file
insatll the req
```bash
pip install -r requirements.txt
```
download the data from

https://drive.google.com/drive/folders/18zqQiCJVgF7uzXgfbIJ-04zgz1ItNfF5?usp=sharing

git init

dvc init

dvc add data_given/winequality.csv

git add .

git commit -m "first commit"

oneliner updates for readme

```
git add . && git commit -m "update Readme.md"
```

git remote add origin https://github.com/malleswarigelli/winequlaity_mlops_dvc.git

git branch -M main

git push -u origin main

