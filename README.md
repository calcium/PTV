# awstools
Miscellaneous tools I used for AWS

## awstools.py
Is actually not AWS specific but a generic tool. It's the template which is product specific.

Example usage : 
```
$ python awstools.py renderTemplate slotType.jinja2 railwaylines.txt
```


## ptv.py
Queries the PTV website.

You need to set your dev-id and key to use this.
It is provided by PTV.

Google APIKeyRequest@ptv.vic.gov.au as to how to request for a set

Example usage : 
```
$ python ptv.py fetchPTV
```
