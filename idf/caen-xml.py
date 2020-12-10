#!/bin/python
import xmlschema

if __name__ == "__main__":
    idf = xmlschema.XMLSchema("idfv1_02.xsd")
    print(idf.is_valid("IAEA25_NDF.xml"))
