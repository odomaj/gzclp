# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: workout.proto
# Protobuf Python Version: 5.28.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    2,
    '',
    'workout.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rworkout.proto\"#\n\x03Set\x12\x0e\n\x06weight\x18\x01 \x01(\x05\x12\x0c\n\x04reps\x18\x02 \x01(\r\"[\n\x08\x45xercise\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08priority\x18\x02 \x01(\r\x12\r\n\x05\x62lock\x18\x03 \x01(\r\x12\x0c\n\x04unit\x18\x04 \x01(\t\x12\x12\n\x04sets\x18\x05 \x03(\x0b\x32\x04.Set\"c\n\x07Workout\x12\r\n\x05month\x18\x01 \x01(\r\x12\x0b\n\x03\x64\x61y\x18\x02 \x01(\r\x12\x0c\n\x04year\x18\x03 \x01(\r\x12\x10\n\x08split_id\x18\x04 \x01(\t\x12\x1c\n\texercises\x18\x05 \x03(\x0b\x32\t.Exerciseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'workout_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_SET']._serialized_start=17
  _globals['_SET']._serialized_end=52
  _globals['_EXERCISE']._serialized_start=54
  _globals['_EXERCISE']._serialized_end=145
  _globals['_WORKOUT']._serialized_start=147
  _globals['_WORKOUT']._serialized_end=246
# @@protoc_insertion_point(module_scope)
