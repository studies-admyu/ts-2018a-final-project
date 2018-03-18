package org.sphere.diploma;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.io.IOUtils;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.compress.CompressionCodec;
import org.apache.hadoop.io.compress.GzipCodec;
import org.apache.hadoop.mapreduce.RecordWriter;
import org.apache.hadoop.mapreduce.TaskAttemptContext;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.ReflectionUtils;
import photo.storage.GenericStorage;

import java.io.DataOutputStream;
import java.io.IOException;

/**
 * Output format class - writes filtered images back to Generic Storage (*.gs) format.
 */
public class StorageOutputFormat extends FileOutputFormat<NullWritable, BytesWritable> {
    /** Extension for Generic Storage formatted files */
    private static final String OUTPUT_FILE_EXTENSION = ".gs";

    /**
     * Record writer class that produces pb2 serialization bytes.
     */
    public class GSRecordWriter extends RecordWriter<NullWritable, BytesWritable> {
        /** Output file stream */
        DataOutputStream _output;

        /**
         * Creates Generic Storage record writer instance.
         * @param output - output stream for the serialization data.
         */
        public GSRecordWriter(DataOutputStream output) {
            // Assign the output stream
            this._output = output;
        }

        @Override
        public void write(NullWritable key, BytesWritable value) throws IOException {
            // Serialize document_length struct with the proper length value
            GenericStorage.document_length document_length_struct = GenericStorage.document_length.newBuilder(
            ).setLength(value.getLength()).build();
            byte[] document_length_bytes = document_length_struct.toByteArray();

            // Write document_length bytes first
            this._output.write(document_length_bytes);
            // Write ImageStruct bytes
            this._output.write(value.getBytes());
        }

        @Override
        public void close(TaskAttemptContext context) {
            IOUtils.closeStream(this._output);
            this._output = null;
        }
    }

    public RecordWriter<NullWritable, BytesWritable> getRecordWriter(TaskAttemptContext context) throws IOException {
        // No compression by default
        CompressionCodec codec = null;
        // Standard extension by default
        String extension = StorageOutputFormat.OUTPUT_FILE_EXTENSION;
        Configuration conf = context.getConfiguration();

        // Check for compression
        if (StorageOutputFormat.getCompressOutput(context)) {
            // Create necessary compression codec instance
            Class<? extends CompressionCodec> codec_class = StorageOutputFormat.getOutputCompressorClass(
                context, GzipCodec.class
            );
            codec = ReflectionUtils.newInstance(codec_class, conf);

            // Modify the output file extension according to compression format
            extension += codec.getDefaultExtension();
        }

        // Open the output file
        Path output_path = this.getDefaultWorkFile(context, extension);
        FileSystem fs = output_path.getFileSystem(conf);
        FSDataOutputStream output = fs.create(output_path, false);

        // Return the record writer
        if (codec != null) {
            return new GSRecordWriter(new DataOutputStream(codec.createOutputStream(output)));
        } else {
            return new GSRecordWriter(output);
        }
    }
}
