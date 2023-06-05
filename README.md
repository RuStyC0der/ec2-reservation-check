# Tool to match reservations with instances
As you may know reservations is just billing abstraction and not linked to any particular instance
This tool will match instances to reservations

Usage:
```
pip install -r requirements.txt

<configure credentials if not confogured yet>

python ./ec2-check-reserved-instances.py
```

Result examples:
```
Reserved instances
+----------------------+---------------------+--------------+--------------+---------------------------+
| Name                 | InstanceId          | InstanceType | OfferingType | ReservedUntil             |
+----------------------+---------------------+--------------+--------------+---------------------------+
| xxxxxxxxxapi.staging | i-01111111111111111 | t3.xlarge    | All Upfront  | 2023-07-08 14:27:21+00:00 |
+----------------------+---------------------+--------------+--------------+---------------------------+

Not reserved instances
+------------------------------+---------------------+--------------+
| Name                         | InstanceId          | InstanceType |
+------------------------------+---------------------+--------------+
| xxxxxxxxxxxx.staging         | i-01111111111111111 | t2.xlarge    |
| xxxxxxxxxxxxent.staging      | i-01111111111111111 | t3.xlarge    |
| xxxxxxxxxxxxtion.staging     | i-01111111111111111 | t3.medium    |
+------------------------------+---------------------+--------------+

No unused reservations found
```

Warning!!! This tool is pretty raw and have some issues:
 - it makes no diference for different reservation types, like dedicated and standart, regional and global.
 - any another issues that are not discovered yet)

PR are welcome
