package org.sphere.diploma;

import com.google.protobuf.InvalidProtocolBufferException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.mapreduce.Mapper;
import photo.bki.ImageBki;

import java.io.IOException;

/**
 * Filtering mapper class.
 * @todo Add face share calculation code & corresponding filtering.
 */
public class MRPhotobankFilterMapper extends Mapper<LongWritable, BytesWritable, NullWritable, BytesWritable> {
    /** Minimum allowed image height option value */
    private int _min_height;
    /** Minimum allowed image width option value */
    private int _min_width;

    @Override
    public void setup(Context context) {
        // Read options' values from the configuration
        Configuration conf = context.getConfiguration();
        this._min_height = conf.getInt(Constants.FILTER_MIN_HEIGHT_OPTION_NAME, Constants.FILTER_MIN_HEIGHT_DEFAULT_VALUE);
        this._min_width = conf.getInt(Constants.FILTER_MIN_WIDTH_OPTION_NAME, Constants.FILTER_MIN_WIDTH_DEFAULT_VALUE);
    }

    @Override
    public void map(LongWritable key, BytesWritable value, Context context) throws IOException, InterruptedException {
        try {
            // Parse ImageStruct bytes
            ImageBki.ImageStruct image_struct = ImageBki.ImageStruct.parseFrom(value.getBytes());

            // Check whenever the image should be allowed
            if ((image_struct.getWidth() >= this._min_width) && (image_struct.getHeight() >= this._min_height)) {
                // Write allowed image to output
                context.write(NullWritable.get(), value);
            }
        } catch (InvalidProtocolBufferException e) {
            // Report read/parsing failure
            context.getCounter(Constants.FILTER_COUNTERS_GROUP_NAME, Constants.DOCUMENTS_READING_FAILED).increment(1);
        }
    }
}
