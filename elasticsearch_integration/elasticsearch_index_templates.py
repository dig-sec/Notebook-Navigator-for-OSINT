{
  "template": {
    "settings": {
      "index": {
        "routing": {
          "allocation": {
            "include": {
              "_tier_preference": "data_content"
            }
          }
        }
      }
    },
    "mappings": {
      "dynamic": "True",
      "dynamic_date_formats": [
        "strict_date_optional_time",
        "yyyy/MM/dd HH:mm:ss Z||yyyy/MM/dd Z"
      ],
      "dynamic_templates": [],
      "date_detection": True,
      "numeric_detection": False,
      "properties": {
        "_shodan": {
          "type": "flattened",
          "index": False
        },
        "ftp": {
          "type": "flattened",
          "index": False
        },
        "geo": {
          "properties": {
            "location": {
              "type": "geo_point",
              "ignore_malformed": True,
              "ignore_z_value": True
            }
          }
        },
        "http": {
          "type": "flattened",
          "index": False,
          "doc_values": False,
          "ignore_above": 8191
        },
        "mac": {
          "type": "flattened",
          "index": False
        },
        "mdns": {
          "type": "flattened",
          "index": False
        },
        "ntp": {
          "type": "flattened",
          "index": False
        },
        "vulns": {
          "type": "flattened",
          "index": False
        }
      }
    },
    "aliases": {}
  }
}