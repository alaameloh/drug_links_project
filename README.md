# Drug linking project

## Usage
the solution is presented as package with entrypoints

`cd` to the root of the repo, and then `pip install . ` 


there are 2 entrypoints : 
- `link_drugs` : generate the expected json output

you can run this with command (at repo root level) :
```
link_drugs -d data/drugs.csv -c data/clinical_trials.csv -pc data/pubmed.csv  -pj data/pubmed.json  -o output.json 
```


- `adhoc_processing`: run the requested adhoc processing

```
adhoc_processing -o output.json 
```

You can also run tests with pytests using (remember to switch to an eventual venv / conda env):
```shell
pip install -r requirements_dev.txt
cd tests
pytest -vv .

```
## Improvements:

- Dockerize the package, and thanks to the structure and already made entrypoints, integrating with job orchestrator (e.g. Argo / Airflow)
won't required any major code refactoring


## Questions : 

- How would you handle large volumes of data (big and / or numerous files ), and what would you change in the code ?

the code as it is uses minimal libraries, and relies mainly and native python and built-ins (I didn't add native python 
parallel execution for readability)

When dealing with larger volumes of data, we'll need something that can scale efficiently, possiblity partinionning and batching 
the data.

=> A go-to solution would be to use pyspark. But to advocate for a framework that I personally used and enjoyed, I'd give 
[Dask](https://www.dask.org/) a try !  
it's practically a native python, compatible with the main ML libraries (e.g. sklearn) and very flexible, robust and 
ergonomic distributed parallel computing framework, requiring much less code refactoring than pyspark
e.g. pandas dataframes with Dask dataframes, Numpy with Dask arrays, etc ...

=> Another solution would be to transform the jobs into APIs that can scale through cloud providers resources

Cheers !