package org.sphere.diploma;

import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.io.IOUtils;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.mapreduce.InputSplit;
import org.apache.hadoop.mapreduce.JobContext;
import org.apache.hadoop.mapreduce.RecordReader;
import org.apache.hadoop.mapreduce.TaskAttemptContext;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import photo.storage.GenericStorage;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * Input format to read generic storage (*.gs) files. Uses protobuf generated classes.
 */
public class StorageInputFormat extends FileInputFormat<LongWritable, BytesWritable> {
    /**
     * Generic storage (*.gs) record reader class.
     */
    public class GSRecordReader extends RecordReader<LongWritable, BytesWritable> {
        /** Estimated size of document_length structure */
        private static final int _DOCUMENT_LENGTH_SIZE = 5;

        /** Overall split start position */
        private long _split_start;
        /** Overall split length in bytes */
        private long _split_length;
        /** Read bytes */
        private long _bytes_read;

        /** Input file stream */
        private FSDataInputStream _input;
        /** Output key */
        private LongWritable _key;
        /** Output value */
        private BytesWritable _value;
        /** Buffer for document_length read bytes */
        private byte[] _document_length_bytes;

        @Override
        public void initialize(InputSplit split, TaskAttemptContext context) throws IOException, InterruptedException {
            // Initialize all the members
            this._bytes_read = 0;
            this._key = new LongWritable(this._bytes_read);
            this._value = new BytesWritable();
            this._document_length_bytes = new byte[_DOCUMENT_LENGTH_SIZE];

            // Get split details
            FileSplit file_split = (FileSplit)split;
            this._split_start = file_split.getStart();
            this._split_length = file_split.getLength();

            // Open input file stream
            Path file_path = file_split.getPath();
            FileSystem file_path_fs = file_path.getFileSystem(context.getConfiguration());
            this._input = file_path_fs.open(file_path);

            // Seek the start point according to split details
            this._input.seek(this._split_start);
        }

        @Override
        public boolean nextKeyValue() throws IOException, InterruptedException {
            // Check for extra available bytes
            if (this._bytes_read >= this._split_length) {
                return false;
            }

            // Read document_length proto2 structure bytes
            IOUtils.readFully(this._input, this._document_length_bytes, 0, this._document_length_bytes.length);
            this._bytes_read += this._document_length_bytes.length;
            // Parse the struct
            GenericStorage.document_length document_length_struct = GenericStorage.document_length.parseFrom(
                this._document_length_bytes
            );

            // Set ImageStruct structure file offset as a key
            this._key.set(this._split_start + this._bytes_read);

            // Preallocate ImageStruct bytes buffer if necessary
            int document_length = document_length_struct.getLength();
            if (this._value.getCapacity() < document_length) {
                this._value.setCapacity(document_length);
            }
            this._value.setSize(document_length);

            // Read ImageStruct bytes as a value
            IOUtils.readFully(this._input, this._value.getBytes(), 0, document_length);
            this._bytes_read += document_length;

            return true;
        }

        @Override
        public LongWritable getCurrentKey() throws IOException, InterruptedException {
            return this._key;
        }

        @Override
        public BytesWritable getCurrentValue() throws IOException, InterruptedException {
            return this._value;
        }

        @Override
        public float getProgress() throws IOException, InterruptedException {
            return (float)this._bytes_read / this._split_length;
        }

        @Override
        public void close() {
            IOUtils.closeStream(this._input);
            this._input = null;
        }
    }

    @Override
    public RecordReader<LongWritable, BytesWritable> createRecordReader(InputSplit split, TaskAttemptContext context) throws IOException, InterruptedException {
        GSRecordReader record_reader = new GSRecordReader();
        record_reader.initialize(split, context);
        return record_reader;
    }

    @Override
    public List<InputSplit> getSplits(JobContext context) throws IOException {
        List<InputSplit> splits = new ArrayList<InputSplit>();

        // Split per file
        for (FileStatus status: this.listStatus(context)) {
            splits.add(new FileSplit(status.getPath(), 0, status.getLen(), null));
        }

        return splits;
    }

    @Override
    protected boolean isSplitable(JobContext context, Path filename) {
        return false;
    }
}
