
 WineQuality Prediction

Application URL : [WineQualtiy Prediction](https://wine-qulaity-app.herokuapp.com/)

## Software and account Requirement/github.com/)
2. [Heroku Account](https://id.heroku.com/login)
3. [VS Code IDE](https://code.visualstudio.com/download)
4. [GIT CLI](https://git-scm.com/downloads)


## Setup


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
```bash
https://drive.google.com/drive/folders/18zqQiCJVgF7uzXgfbIJ-04zgz1ItNfF5?usp=sharing
```
```bash
git init
```

```
dvc init
```

```
dvc add data_given/winequality.csv
```

```bash
git add .

git commit -m "first commit"
```

oneliner updates for readme

```
git add . && git commit -m "update Readme.md"
```

```bash
git remote add origin https://github.com/malleswarigelli/winequlaity_mlops_dvc.git
```

```bash
git branch -M main
```

```bash
git push -u origin main
```

tox command 
```bash
tox
```

for rebuilding -
```bash
tox -r
```

pytest command
```bash
pytest -v
```

setup commands .
pip install -e .


build your own package commands.
```bash
python setup.py sdist ddist_wheel
```