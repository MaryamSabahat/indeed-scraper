# Indeed-scraper

# Requirements

* Python version > 3.9
* MySQL databse with 2 tables

# Build/load

``` bash
python3.11 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

playwright install
```

Berofe runnig need to fell up <code>.env</code> file.<br>
<code>.env.dist</code> file as exemple.

# Run/Collect
## Collect all datas
To collect all reviews from each comany run:
```bash
./collect_all.sh
``` 

## Collect new datas
To collect new reviews from each comany for current day run:
```bash
./collect_new.sh
``` 