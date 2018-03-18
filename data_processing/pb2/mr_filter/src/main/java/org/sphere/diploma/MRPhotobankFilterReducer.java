package org.sphere.diploma;

import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

/**
 * Proxy reducer - just passes the output ot output part file.
 */
public class MRPhotobankFilterReducer extends Reducer<NullWritable, BytesWritable, NullWritable, BytesWritable> {

    @Override
    public void reduce(NullWritable key, Iterable<BytesWritable> values, Context context) throws IOException, InterruptedException {
        // Pass all the output to output part file
        for (BytesWritable document_bytes: values) {
            context.write(NullWritable.get(), document_bytes);
        }
    }
}
