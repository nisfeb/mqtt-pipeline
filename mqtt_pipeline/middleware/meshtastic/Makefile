# Default target
all: proto

# Generate Python code from Protocol Buffer definitions
proto:
	cd ./protobufs && protoc --proto_path=. --python_out=. meshtastic/*.proto
	# Then fix the imports with a script
	python fix_protobuf_imports.py

# Clean generated Python files (optional)
clean:
	cd ./protobufs && rm -f ./meshtastic/*_pb2.py

.PHONY: all proto clean
