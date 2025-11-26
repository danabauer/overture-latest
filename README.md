# Overture Maps Latest Release

Displays the latest Overture Maps data release version with quick-copy paths to S3 and Azure. Fetches (weekly) the available release versions from the [STAC catalog](https://stac.overturemaps.org/catalog.json) and regenerates [this page](https://danabauer.github.io/overture-latest/).

## You too can fetch the latest Overture data release version!

**Using Python (pystac) to lookup latest in Overture's STAC catalog:**

```python
import pystac

catalog = pystac.Catalog.from_file("https://stac.overturemaps.org/catalog.json")
latest = catalog.extra_fields["latest"] #latest is custom Overture property
```

**Using Python (obstore) to pull the latest release version directly from S3:**

```python
from obstore.store import S3Store

store = S3Store("overturemaps-us-west-2", region="us-west-2", skip_signature=True)
releases = store.list_with_delimiter("release/")["common_prefixes"]
latest = sorted(releases, reverse=True)[0].strip("release/")
```
**DuckDB:**

```sql
select latest from read_json('https://stac.overturemaps.org/catalog.json');
```

```sql
-- set a variable called latest with the latest release version
set variable latest=(select latest from read_json('https://stac.overturemaps.org/catalog.json'));

-- use latest in your S3 endpoint to query the total number of POIs in the current release
select count(1) from read_parquet('s3://overturemaps-us-west-2/release/' || getvariable('latest') || '/theme=places/type=place/*');
```

**curl:**

```bash
curl -s https://stac.overturemaps.org | jq '.latest'
```
