# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: meshtastic/apponly.proto
# Protobuf Python Version: 5.29.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    2,
    '',
    'meshtastic/apponly.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import channel_pb2 as meshtastic_dot_channel__pb2
from . import config_pb2 as meshtastic_dot_config__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18meshtastic/apponly.proto\x12\nmeshtastic\x1a\x18meshtastic/channel.proto\x1a\x17meshtastic/config.proto\"o\n\nChannelSet\x12-\n\x08settings\x18\x01 \x03(\x0b\x32\x1b.meshtastic.ChannelSettings\x12\x32\n\x0blora_config\x18\x02 \x01(\x0b\x32\x1d.meshtastic.Config.LoRaConfigBb\n\x13\x63om.geeksville.meshB\rAppOnlyProtosZ\"github.com/meshtastic/go/generated\xaa\x02\x14Meshtastic.Protobufs\xba\x02\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'meshtastic.apponly_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\023com.geeksville.meshB\rAppOnlyProtosZ\"github.com/meshtastic/go/generated\252\002\024Meshtastic.Protobufs\272\002\000'
  _globals['_CHANNELSET']._serialized_start=91
  _globals['_CHANNELSET']._serialized_end=202
# @@protoc_insertion_point(module_scope)
