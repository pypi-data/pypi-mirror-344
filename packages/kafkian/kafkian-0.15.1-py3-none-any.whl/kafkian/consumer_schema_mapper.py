import inspect
import typing

from kafkian.producer import PydanticKafkaMessageBaseMixin, SerializationFormat


def get_schema_classes(module: typing.Any):
    schema_to_class = {}
    for name, kls in inspect.getmembers(module):
        if inspect.isclass(kls) and issubclass(kls, PydanticKafkaMessageBaseMixin):
            print(name, kls)
            if kls.Config.serialization_format == SerializationFormat.JSON:
                schema_to_class[name] = kls
            elif kls.Config.serialization_format == SerializationFormat.AVRO:
                schema_to_class[kls.Config.schema.full_name] = kls
            elif kls.Config.serialization_format == SerializationFormat.PROTOBUF:
                schema_to_class[kls.Config.schema.name] = kls

    return schema_to_class
