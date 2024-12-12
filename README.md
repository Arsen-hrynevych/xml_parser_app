**XML Parser App**

This project is an XML parser application built without using any external packages. (mako file also)

To pretty-print the result, you can add:

```
import json
print(json.dumps(parsed_xml_result, indent=4))
```

### Starting the project for parsing:

1. Build the Docker image:
    ```
    docker build -t xml_parcel_app .
    ```
2. Run the Docker container in **main mode**:
    ```
    docker run -e APP_MODE=main --name xml_parcel_app
    ```
3. Remove the Docker container:
    ```
    docker remove xml_parcel_app
    ```

### Starting the project for testing:

1. Build the Docker image:
    ```
    docker build -t xml_parcel_app .
    ```
2. Run the Docker container in **test mode**:
    ```
    docker run -e APP_MODE=test --name xml_parcel_app
    ```
3. Remove the Docker container:
    ```
    docker remove xml_parcel_app
    ```

### Performance Information (Time Taken Based on XML Size):

For small XML data:

```xml
<root>
  <user>
    <email>123@gmail.com</email>
    <name>name1</name>
  </user>
  <user>
    <email>321@gmail.com</email>
    <name>name2</name>
  </user>
  <user>
    <value1>1</value1>
    <value2>2</value2>
    <meta>
      <date>today</date>
      <x>33</x>
    </meta>
  </user>
</root>
```

On a MacBook Pro with 16GB RAM and M1 Pro chip, parsing this small XML takes:
- **Time taken**: 0.000045 seconds - 0.000029 seconds.

For larger XML data (e.g., 100,000 user entries):

On the same MacBook Pro, parsing a larger XML with 100,000 users takes:
- **Time taken**: 0.050716 seconds - 0.048880 seconds.
