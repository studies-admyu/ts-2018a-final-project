package org.sphere.diploma;

import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.mapreduce.Partitioner;

/**
 * Filtering partitioner - balances output images size in output part files.
 */
public class MRPhotobankFilterPartitioner extends Partitioner<NullWritable, BytesWritable> {

    @Override
    public int getPartition(NullWritable key, BytesWritable value, int number_of_partitions) {
        return Math.abs(value.hashCode()) % number_of_partitions;
    }
}
