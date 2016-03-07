package com.kjw.artedu;

import android.os.Bundle;
import android.os.Environment;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.io.File;
import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {
    TextView mProgressTv;
    Button mUploadButton;
    OkHttpClient mClient;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        mProgressTv = (TextView) findViewById(R.id.progressTv);
        mUploadButton = (Button) findViewById(R.id.upload);
        mClient = new OkHttpClient();
        mUploadButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                upload();
            }
        });

    }

    private void upload() {
        File file = new File(Environment.getExternalStorageDirectory() + "/log.txt");
        //此文件必须在手机上存在，实际情况下请自行修改，这个目录下的文件只是在我手机中存在。


        //这个是非ui线程回调，不可直接操作UI
        final ProgressRequestListener progressListener = new ProgressRequestListener() {
            @Override
            public void onRequestProgress(long bytesWrite, long contentLength, boolean done) {
                Log.e("ProgressRequestListener", "bytesWrite:" + bytesWrite);
                Log.e("ProgressRequestListener", "contentLength" + contentLength);
                Log.e("ProgressRequestListener", (100 * bytesWrite) / contentLength + " % done ");
                Log.e("ProgressRequestListener", "done:" + done);
                Log.e("ProgressRequestListener", "================================");
            }
        };


        //这个是ui线程回调，可直接操作UI
        final UIProgressListener uiProgressRequestListener = new UIProgressListener() {
            @Override
            public void onUIRequestProgress(long bytesWrite, long contentLength, boolean done) {
                Log.e("UIProgressListener", "bytesWrite:" + bytesWrite);
                Log.e("UIProgressListener", "contentLength" + contentLength);
                Log.e("UIProgressListener", (100 * bytesWrite) / contentLength + " % done ");
                Log.e("UIProgressListener", "done:" + done);
                Log.e("UIProgressListener", "================================");
                //ui层回调
                mProgressTv.setText(String.valueOf((100 * bytesWrite / contentLength)) + "%");
                //Toast.makeText(getApplicationContext(), bytesWrite + " " + contentLength + " " + done, Toast.LENGTH_LONG).show();
            }
        };

        //构造上传请求，类似web表单
        RequestBody fileBody = RequestBody.create(null, "");
        RequestBody requestBody = new MultipartBody.Builder()
                .setType(MultipartBody.FORM)
                .addFormDataPart("myfile", file.getName(), fileBody)
                .addFormDataPart("myfile", "123123", RequestBody.create(null,"12123123"))
                .build();


        //进行包装，使其支持进度回调
        final Request request = new Request.Builder().url("http://10.70.148.137:8011/upload")
                .post(ProgressRequestBody.addProgressRequestListener(requestBody, uiProgressRequestListener))
                .build();
        //开始请求
        mClient.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                Log.e("TAG", "error ", e);
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                Log.e("TAG", response.body().string());
            }
        });
    }

}
