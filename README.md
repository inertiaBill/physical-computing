# physical-computing
Computer interaction with the real world

Temperature monitor (sheet_access.py)

Inserts current temperations in a Google Sheet. The sheet and sensor indentifiers are specified using environment variables.

https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid=0

```
export SOLAR_SPREADSHEET={spreadsheet_id_from_URL}
export SOLAR_SHEET={label_of_sheet_tab}
export SOLAR_RANGE=A2:E
export THERMAL_PROB=/sys/bus/w1/devices/28-000007bb1844/w1_slave
export THERMAL_SENSOR=/sys/bus/w1/devices/28-000007ba00af/w1_slave
```

# Prepare virtual environment

Active virtual environment.

Install gpiozero.
- `pip3 install gpiozero`

# Troubleshooting

If you see,

```
google.auth.exceptions.RefreshError: ('invalid_grant: Token has been expired or revoked.', '{\n  "error": "invalid_grant",\n  "error_description": "Token has been expired or revoked."\n}')
```

Remove token.pickle 
