#!/usr/bin/env bash
# Create basic Orion entities for testing
ORION=${ORION_HOST:-http:// 172.23.48.1:1026}

echo "Creating Mission:Current and Zone:Kitchen in Orion at ${ORION}"

# Mission:Current (upsert - ignore errors)
curl -s -X POST "${ORION}/v2/entities" -H "Content-Type: application/json" -d '{
  "id": "Mission:Current",
  "type": "Mission",
  "status": { "type": "Text", "value": "idle" },
  "target": { "type":"StructuredValue", "value": {"x": 0.0, "y": 0.0, "frame":"map"} }
}' || true

# Zone:Kitchen
curl -s -X POST "${ORION}/v2/entities" -H "Content-Type: application/json" -d '{
  "id": "Zone:Kitchen",
  "type": "Zone",
  "name": { "type": "Text", "value": "Kitchen" },
  "coordinates": { "type":"StructuredValue", "value": {"x": 5.0, "y": 3.0} }
}' || true

echo "Entities created (or already existed)."
