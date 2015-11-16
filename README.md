Streaming Server

cd ./test

1.start relay server
@192.168.0.103

./qtpasswd newuser -A pushuser 
./DarwinStreamingServer -c streamingserver.xml -d

2.start push server
@192.168.0.51

ffmpeg -i rtsp://admin:MCeltAPuwpGjoUcz@192.168.74.21:554/ -vcodec copy -acodec copy  -rtsp_transport tcp -f rtsp rtsp://Quser:111111@192.168.0.103:8554/test.sdp

3.play rtsp
@192.168.0.103

ffplay rtsp://viewer:222222@192.168.0.103:7070/test.sdp
