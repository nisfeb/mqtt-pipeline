# Default target
all: proto

# Generate Python code from Protocol Buffer definitions
proto:
	cd ./protobufs && protoc --python_out=./ ./meshtastic/*.proto

# Clean generated Python files (optional)
clean:
	cd ./protobufs && rm -f ./meshtastic/*_pb2.py

.PHONY: all proto clean
