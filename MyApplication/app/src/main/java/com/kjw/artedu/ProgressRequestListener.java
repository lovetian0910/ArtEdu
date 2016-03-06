package com.kjw.artedu;

/**
 * Created by Administrator on 2016/3/6.
 */
public interface ProgressRequestListener {
    void onRequestProgress(long bytesWritten, long contentLength, boolean done);
}
