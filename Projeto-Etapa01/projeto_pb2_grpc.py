# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import projeto_pb2 as projeto__pb2


class AdminPortalStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateClient = channel.unary_unary(
                '/project.AdminPortal/CreateClient',
                request_serializer=projeto__pb2.Client.SerializeToString,
                response_deserializer=projeto__pb2.Reply.FromString,
                )
        self.RetrieveClient = channel.unary_unary(
                '/project.AdminPortal/RetrieveClient',
                request_serializer=projeto__pb2.ID.SerializeToString,
                response_deserializer=projeto__pb2.Client.FromString,
                )
        self.UpdateClient = channel.unary_unary(
                '/project.AdminPortal/UpdateClient',
                request_serializer=projeto__pb2.Client.SerializeToString,
                response_deserializer=projeto__pb2.Reply.FromString,
                )
        self.DeleteClient = channel.unary_unary(
                '/project.AdminPortal/DeleteClient',
                request_serializer=projeto__pb2.ID.SerializeToString,
                response_deserializer=projeto__pb2.Reply.FromString,
                )
        self.CreateProduct = channel.unary_unary(
                '/project.AdminPortal/CreateProduct',
                request_serializer=projeto__pb2.Product.SerializeToString,
                response_deserializer=projeto__pb2.Reply.FromString,
                )
        self.RetrieveProduct = channel.unary_unary(
                '/project.AdminPortal/RetrieveProduct',
                request_serializer=projeto__pb2.ID.SerializeToString,
                response_deserializer=projeto__pb2.Product.FromString,
                )
        self.UpdateProduct = channel.unary_unary(
                '/project.AdminPortal/UpdateProduct',
                request_serializer=projeto__pb2.Product.SerializeToString,
                response_deserializer=projeto__pb2.Reply.FromString,
                )
        self.DeleteProduct = channel.unary_unary(
                '/project.AdminPortal/DeleteProduct',
                request_serializer=projeto__pb2.ID.SerializeToString,
                response_deserializer=projeto__pb2.Reply.FromString,
                )


class AdminPortalServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateClient(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RetrieveClient(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateClient(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteClient(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateProduct(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RetrieveProduct(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateProduct(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteProduct(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AdminPortalServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateClient': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateClient,
                    request_deserializer=projeto__pb2.Client.FromString,
                    response_serializer=projeto__pb2.Reply.SerializeToString,
            ),
            'RetrieveClient': grpc.unary_unary_rpc_method_handler(
                    servicer.RetrieveClient,
                    request_deserializer=projeto__pb2.ID.FromString,
                    response_serializer=projeto__pb2.Client.SerializeToString,
            ),
            'UpdateClient': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateClient,
                    request_deserializer=projeto__pb2.Client.FromString,
                    response_serializer=projeto__pb2.Reply.SerializeToString,
            ),
            'DeleteClient': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteClient,
                    request_deserializer=projeto__pb2.ID.FromString,
                    response_serializer=projeto__pb2.Reply.SerializeToString,
            ),
            'CreateProduct': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateProduct,
                    request_deserializer=projeto__pb2.Product.FromString,
                    response_serializer=projeto__pb2.Reply.SerializeToString,
            ),
            'RetrieveProduct': grpc.unary_unary_rpc_method_handler(
                    servicer.RetrieveProduct,
                    request_deserializer=projeto__pb2.ID.FromString,
                    response_serializer=projeto__pb2.Product.SerializeToString,
            ),
            'UpdateProduct': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateProduct,
                    request_deserializer=projeto__pb2.Product.FromString,
                    response_serializer=projeto__pb2.Reply.SerializeToString,
            ),
            'DeleteProduct': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteProduct,
                    request_deserializer=projeto__pb2.ID.FromString,
                    response_serializer=projeto__pb2.Reply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'project.AdminPortal', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AdminPortal(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateClient(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/project.AdminPortal/CreateClient',
            projeto__pb2.Client.SerializeToString,
            projeto__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RetrieveClient(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/project.AdminPortal/RetrieveClient',
            projeto__pb2.ID.SerializeToString,
            projeto__pb2.Client.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateClient(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/project.AdminPortal/UpdateClient',
            projeto__pb2.Client.SerializeToString,
            projeto__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteClient(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/project.AdminPortal/DeleteClient',
            projeto__pb2.ID.SerializeToString,
            projeto__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateProduct(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/project.AdminPortal/CreateProduct',
            projeto__pb2.Product.SerializeToString,
            projeto__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RetrieveProduct(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/project.AdminPortal/RetrieveProduct',
            projeto__pb2.ID.SerializeToString,
            projeto__pb2.Product.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateProduct(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/project.AdminPortal/UpdateProduct',
            projeto__pb2.Product.SerializeToString,
            projeto__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteProduct(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/project.AdminPortal/DeleteProduct',
            projeto__pb2.ID.SerializeToString,
            projeto__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class OrderPortalStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateOrder = channel.unary_unary(
                '/project.OrderPortal/CreateOrder',
                request_serializer=projeto__pb2.Order.SerializeToString,
                response_deserializer=projeto__pb2.Reply.FromString,
                )
        self.RetrieveOrder = channel.unary_unary(
                '/project.OrderPortal/RetrieveOrder',
                request_serializer=projeto__pb2.ID.SerializeToString,
                response_deserializer=projeto__pb2.Order.FromString,
                )
        self.UpdateOrder = channel.unary_unary(
                '/project.OrderPortal/UpdateOrder',
                request_serializer=projeto__pb2.Order.SerializeToString,
                response_deserializer=projeto__pb2.Reply.FromString,
                )
        self.DeleteOrder = channel.unary_unary(
                '/project.OrderPortal/DeleteOrder',
                request_serializer=projeto__pb2.ID.SerializeToString,
                response_deserializer=projeto__pb2.Reply.FromString,
                )
        self.RetrieveClientOrders = channel.unary_stream(
                '/project.OrderPortal/RetrieveClientOrders',
                request_serializer=projeto__pb2.ID.SerializeToString,
                response_deserializer=projeto__pb2.Order.FromString,
                )


class OrderPortalServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateOrder(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RetrieveOrder(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateOrder(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteOrder(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RetrieveClientOrders(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OrderPortalServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateOrder': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateOrder,
                    request_deserializer=projeto__pb2.Order.FromString,
                    response_serializer=projeto__pb2.Reply.SerializeToString,
            ),
            'RetrieveOrder': grpc.unary_unary_rpc_method_handler(
                    servicer.RetrieveOrder,
                    request_deserializer=projeto__pb2.ID.FromString,
                    response_serializer=projeto__pb2.Order.SerializeToString,
            ),
            'UpdateOrder': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateOrder,
                    request_deserializer=projeto__pb2.Order.FromString,
                    response_serializer=projeto__pb2.Reply.SerializeToString,
            ),
            'DeleteOrder': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteOrder,
                    request_deserializer=projeto__pb2.ID.FromString,
                    response_serializer=projeto__pb2.Reply.SerializeToString,
            ),
            'RetrieveClientOrders': grpc.unary_stream_rpc_method_handler(
                    servicer.RetrieveClientOrders,
                    request_deserializer=projeto__pb2.ID.FromString,
                    response_serializer=projeto__pb2.Order.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'project.OrderPortal', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class OrderPortal(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateOrder(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/project.OrderPortal/CreateOrder',
            projeto__pb2.Order.SerializeToString,
            projeto__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RetrieveOrder(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/project.OrderPortal/RetrieveOrder',
            projeto__pb2.ID.SerializeToString,
            projeto__pb2.Order.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateOrder(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/project.OrderPortal/UpdateOrder',
            projeto__pb2.Order.SerializeToString,
            projeto__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteOrder(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/project.OrderPortal/DeleteOrder',
            projeto__pb2.ID.SerializeToString,
            projeto__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RetrieveClientOrders(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/project.OrderPortal/RetrieveClientOrders',
            projeto__pb2.ID.SerializeToString,
            projeto__pb2.Order.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
