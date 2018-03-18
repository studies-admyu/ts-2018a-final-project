// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: gs.proto

package photo.storage;

public final class GenericStorage {
  private GenericStorage() {}
  public static void registerAllExtensions(
      com.google.protobuf.ExtensionRegistry registry) {
  }
  public interface document_lengthOrBuilder
      extends com.google.protobuf.MessageOrBuilder {

    // required fixed32 length = 1;
    /**
     * <code>required fixed32 length = 1;</code>
     */
    boolean hasLength();
    /**
     * <code>required fixed32 length = 1;</code>
     */
    int getLength();
  }
  /**
   * Protobuf type {@code photo.storage.document_length}
   */
  public static final class document_length extends
      com.google.protobuf.GeneratedMessage
      implements document_lengthOrBuilder {
    // Use document_length.newBuilder() to construct.
    private document_length(com.google.protobuf.GeneratedMessage.Builder<?> builder) {
      super(builder);
      this.unknownFields = builder.getUnknownFields();
    }
    private document_length(boolean noInit) { this.unknownFields = com.google.protobuf.UnknownFieldSet.getDefaultInstance(); }

    private static final document_length defaultInstance;
    public static document_length getDefaultInstance() {
      return defaultInstance;
    }

    public document_length getDefaultInstanceForType() {
      return defaultInstance;
    }

    private final com.google.protobuf.UnknownFieldSet unknownFields;
    @java.lang.Override
    public final com.google.protobuf.UnknownFieldSet
        getUnknownFields() {
      return this.unknownFields;
    }
    private document_length(
        com.google.protobuf.CodedInputStream input,
        com.google.protobuf.ExtensionRegistryLite extensionRegistry)
        throws com.google.protobuf.InvalidProtocolBufferException {
      initFields();
      int mutable_bitField0_ = 0;
      com.google.protobuf.UnknownFieldSet.Builder unknownFields =
          com.google.protobuf.UnknownFieldSet.newBuilder();
      try {
        boolean done = false;
        while (!done) {
          int tag = input.readTag();
          switch (tag) {
            case 0:
              done = true;
              break;
            default: {
              if (!parseUnknownField(input, unknownFields,
                                     extensionRegistry, tag)) {
                done = true;
              }
              break;
            }
            case 13: {
              bitField0_ |= 0x00000001;
              length_ = input.readFixed32();
              break;
            }
          }
        }
      } catch (com.google.protobuf.InvalidProtocolBufferException e) {
        throw e.setUnfinishedMessage(this);
      } catch (java.io.IOException e) {
        throw new com.google.protobuf.InvalidProtocolBufferException(
            e.getMessage()).setUnfinishedMessage(this);
      } finally {
        this.unknownFields = unknownFields.build();
        makeExtensionsImmutable();
      }
    }
    public static final com.google.protobuf.Descriptors.Descriptor
        getDescriptor() {
      return photo.storage.GenericStorage.internal_static_photo_storage_document_length_descriptor;
    }

    protected com.google.protobuf.GeneratedMessage.FieldAccessorTable
        internalGetFieldAccessorTable() {
      return photo.storage.GenericStorage.internal_static_photo_storage_document_length_fieldAccessorTable
          .ensureFieldAccessorsInitialized(
              photo.storage.GenericStorage.document_length.class, photo.storage.GenericStorage.document_length.Builder.class);
    }

    public static com.google.protobuf.Parser<document_length> PARSER =
        new com.google.protobuf.AbstractParser<document_length>() {
      public document_length parsePartialFrom(
          com.google.protobuf.CodedInputStream input,
          com.google.protobuf.ExtensionRegistryLite extensionRegistry)
          throws com.google.protobuf.InvalidProtocolBufferException {
        return new document_length(input, extensionRegistry);
      }
    };

    @java.lang.Override
    public com.google.protobuf.Parser<document_length> getParserForType() {
      return PARSER;
    }

    private int bitField0_;
    // required fixed32 length = 1;
    public static final int LENGTH_FIELD_NUMBER = 1;
    private int length_;
    /**
     * <code>required fixed32 length = 1;</code>
     */
    public boolean hasLength() {
      return ((bitField0_ & 0x00000001) == 0x00000001);
    }
    /**
     * <code>required fixed32 length = 1;</code>
     */
    public int getLength() {
      return length_;
    }

    private void initFields() {
      length_ = 0;
    }
    private byte memoizedIsInitialized = -1;
    public final boolean isInitialized() {
      byte isInitialized = memoizedIsInitialized;
      if (isInitialized != -1) return isInitialized == 1;

      if (!hasLength()) {
        memoizedIsInitialized = 0;
        return false;
      }
      memoizedIsInitialized = 1;
      return true;
    }

    public void writeTo(com.google.protobuf.CodedOutputStream output)
                        throws java.io.IOException {
      getSerializedSize();
      if (((bitField0_ & 0x00000001) == 0x00000001)) {
        output.writeFixed32(1, length_);
      }
      getUnknownFields().writeTo(output);
    }

    private int memoizedSerializedSize = -1;
    public int getSerializedSize() {
      int size = memoizedSerializedSize;
      if (size != -1) return size;

      size = 0;
      if (((bitField0_ & 0x00000001) == 0x00000001)) {
        size += com.google.protobuf.CodedOutputStream
          .computeFixed32Size(1, length_);
      }
      size += getUnknownFields().getSerializedSize();
      memoizedSerializedSize = size;
      return size;
    }

    private static final long serialVersionUID = 0L;
    @java.lang.Override
    protected java.lang.Object writeReplace()
        throws java.io.ObjectStreamException {
      return super.writeReplace();
    }

    public static photo.storage.GenericStorage.document_length parseFrom(
        com.google.protobuf.ByteString data)
        throws com.google.protobuf.InvalidProtocolBufferException {
      return PARSER.parseFrom(data);
    }
    public static photo.storage.GenericStorage.document_length parseFrom(
        com.google.protobuf.ByteString data,
        com.google.protobuf.ExtensionRegistryLite extensionRegistry)
        throws com.google.protobuf.InvalidProtocolBufferException {
      return PARSER.parseFrom(data, extensionRegistry);
    }
    public static photo.storage.GenericStorage.document_length parseFrom(byte[] data)
        throws com.google.protobuf.InvalidProtocolBufferException {
      return PARSER.parseFrom(data);
    }
    public static photo.storage.GenericStorage.document_length parseFrom(
        byte[] data,
        com.google.protobuf.ExtensionRegistryLite extensionRegistry)
        throws com.google.protobuf.InvalidProtocolBufferException {
      return PARSER.parseFrom(data, extensionRegistry);
    }
    public static photo.storage.GenericStorage.document_length parseFrom(java.io.InputStream input)
        throws java.io.IOException {
      return PARSER.parseFrom(input);
    }
    public static photo.storage.GenericStorage.document_length parseFrom(
        java.io.InputStream input,
        com.google.protobuf.ExtensionRegistryLite extensionRegistry)
        throws java.io.IOException {
      return PARSER.parseFrom(input, extensionRegistry);
    }
    public static photo.storage.GenericStorage.document_length parseDelimitedFrom(java.io.InputStream input)
        throws java.io.IOException {
      return PARSER.parseDelimitedFrom(input);
    }
    public static photo.storage.GenericStorage.document_length parseDelimitedFrom(
        java.io.InputStream input,
        com.google.protobuf.ExtensionRegistryLite extensionRegistry)
        throws java.io.IOException {
      return PARSER.parseDelimitedFrom(input, extensionRegistry);
    }
    public static photo.storage.GenericStorage.document_length parseFrom(
        com.google.protobuf.CodedInputStream input)
        throws java.io.IOException {
      return PARSER.parseFrom(input);
    }
    public static photo.storage.GenericStorage.document_length parseFrom(
        com.google.protobuf.CodedInputStream input,
        com.google.protobuf.ExtensionRegistryLite extensionRegistry)
        throws java.io.IOException {
      return PARSER.parseFrom(input, extensionRegistry);
    }

    public static Builder newBuilder() { return Builder.create(); }
    public Builder newBuilderForType() { return newBuilder(); }
    public static Builder newBuilder(photo.storage.GenericStorage.document_length prototype) {
      return newBuilder().mergeFrom(prototype);
    }
    public Builder toBuilder() { return newBuilder(this); }

    @java.lang.Override
    protected Builder newBuilderForType(
        com.google.protobuf.GeneratedMessage.BuilderParent parent) {
      Builder builder = new Builder(parent);
      return builder;
    }
    /**
     * Protobuf type {@code photo.storage.document_length}
     */
    public static final class Builder extends
        com.google.protobuf.GeneratedMessage.Builder<Builder>
       implements photo.storage.GenericStorage.document_lengthOrBuilder {
      public static final com.google.protobuf.Descriptors.Descriptor
          getDescriptor() {
        return photo.storage.GenericStorage.internal_static_photo_storage_document_length_descriptor;
      }

      protected com.google.protobuf.GeneratedMessage.FieldAccessorTable
          internalGetFieldAccessorTable() {
        return photo.storage.GenericStorage.internal_static_photo_storage_document_length_fieldAccessorTable
            .ensureFieldAccessorsInitialized(
                photo.storage.GenericStorage.document_length.class, photo.storage.GenericStorage.document_length.Builder.class);
      }

      // Construct using photo.storage.GenericStorage.document_length.newBuilder()
      private Builder() {
        maybeForceBuilderInitialization();
      }

      private Builder(
          com.google.protobuf.GeneratedMessage.BuilderParent parent) {
        super(parent);
        maybeForceBuilderInitialization();
      }
      private void maybeForceBuilderInitialization() {
        if (com.google.protobuf.GeneratedMessage.alwaysUseFieldBuilders) {
        }
      }
      private static Builder create() {
        return new Builder();
      }

      public Builder clear() {
        super.clear();
        length_ = 0;
        bitField0_ = (bitField0_ & ~0x00000001);
        return this;
      }

      public Builder clone() {
        return create().mergeFrom(buildPartial());
      }

      public com.google.protobuf.Descriptors.Descriptor
          getDescriptorForType() {
        return photo.storage.GenericStorage.internal_static_photo_storage_document_length_descriptor;
      }

      public photo.storage.GenericStorage.document_length getDefaultInstanceForType() {
        return photo.storage.GenericStorage.document_length.getDefaultInstance();
      }

      public photo.storage.GenericStorage.document_length build() {
        photo.storage.GenericStorage.document_length result = buildPartial();
        if (!result.isInitialized()) {
          throw newUninitializedMessageException(result);
        }
        return result;
      }

      public photo.storage.GenericStorage.document_length buildPartial() {
        photo.storage.GenericStorage.document_length result = new photo.storage.GenericStorage.document_length(this);
        int from_bitField0_ = bitField0_;
        int to_bitField0_ = 0;
        if (((from_bitField0_ & 0x00000001) == 0x00000001)) {
          to_bitField0_ |= 0x00000001;
        }
        result.length_ = length_;
        result.bitField0_ = to_bitField0_;
        onBuilt();
        return result;
      }

      public Builder mergeFrom(com.google.protobuf.Message other) {
        if (other instanceof photo.storage.GenericStorage.document_length) {
          return mergeFrom((photo.storage.GenericStorage.document_length)other);
        } else {
          super.mergeFrom(other);
          return this;
        }
      }

      public Builder mergeFrom(photo.storage.GenericStorage.document_length other) {
        if (other == photo.storage.GenericStorage.document_length.getDefaultInstance()) return this;
        if (other.hasLength()) {
          setLength(other.getLength());
        }
        this.mergeUnknownFields(other.getUnknownFields());
        return this;
      }

      public final boolean isInitialized() {
        if (!hasLength()) {
          
          return false;
        }
        return true;
      }

      public Builder mergeFrom(
          com.google.protobuf.CodedInputStream input,
          com.google.protobuf.ExtensionRegistryLite extensionRegistry)
          throws java.io.IOException {
        photo.storage.GenericStorage.document_length parsedMessage = null;
        try {
          parsedMessage = PARSER.parsePartialFrom(input, extensionRegistry);
        } catch (com.google.protobuf.InvalidProtocolBufferException e) {
          parsedMessage = (photo.storage.GenericStorage.document_length) e.getUnfinishedMessage();
          throw e;
        } finally {
          if (parsedMessage != null) {
            mergeFrom(parsedMessage);
          }
        }
        return this;
      }
      private int bitField0_;

      // required fixed32 length = 1;
      private int length_ ;
      /**
       * <code>required fixed32 length = 1;</code>
       */
      public boolean hasLength() {
        return ((bitField0_ & 0x00000001) == 0x00000001);
      }
      /**
       * <code>required fixed32 length = 1;</code>
       */
      public int getLength() {
        return length_;
      }
      /**
       * <code>required fixed32 length = 1;</code>
       */
      public Builder setLength(int value) {
        bitField0_ |= 0x00000001;
        length_ = value;
        onChanged();
        return this;
      }
      /**
       * <code>required fixed32 length = 1;</code>
       */
      public Builder clearLength() {
        bitField0_ = (bitField0_ & ~0x00000001);
        length_ = 0;
        onChanged();
        return this;
      }

      // @@protoc_insertion_point(builder_scope:photo.storage.document_length)
    }

    static {
      defaultInstance = new document_length(true);
      defaultInstance.initFields();
    }

    // @@protoc_insertion_point(class_scope:photo.storage.document_length)
  }

  private static com.google.protobuf.Descriptors.Descriptor
    internal_static_photo_storage_document_length_descriptor;
  private static
    com.google.protobuf.GeneratedMessage.FieldAccessorTable
      internal_static_photo_storage_document_length_fieldAccessorTable;

  public static com.google.protobuf.Descriptors.FileDescriptor
      getDescriptor() {
    return descriptor;
  }
  private static com.google.protobuf.Descriptors.FileDescriptor
      descriptor;
  static {
    java.lang.String[] descriptorData = {
      "\n\010gs.proto\022\rphoto.storage\"!\n\017document_le" +
      "ngth\022\016\n\006length\030\001 \002(\007B\020B\016GenericStorage"
    };
    com.google.protobuf.Descriptors.FileDescriptor.InternalDescriptorAssigner assigner =
      new com.google.protobuf.Descriptors.FileDescriptor.InternalDescriptorAssigner() {
        public com.google.protobuf.ExtensionRegistry assignDescriptors(
            com.google.protobuf.Descriptors.FileDescriptor root) {
          descriptor = root;
          internal_static_photo_storage_document_length_descriptor =
            getDescriptor().getMessageTypes().get(0);
          internal_static_photo_storage_document_length_fieldAccessorTable = new
            com.google.protobuf.GeneratedMessage.FieldAccessorTable(
              internal_static_photo_storage_document_length_descriptor,
              new java.lang.String[] { "Length", });
          return null;
        }
      };
    com.google.protobuf.Descriptors.FileDescriptor
      .internalBuildGeneratedFileFrom(descriptorData,
        new com.google.protobuf.Descriptors.FileDescriptor[] {
        }, assigner);
  }

  // @@protoc_insertion_point(outer_class_scope)
}