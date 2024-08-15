import android.media.AudioFormat;
import android.media.AudioManager;
import android.media.AudioTrack;
import android.os.AsyncTask;
import java.net.DatagramPacket;
import java.net.DatagramSocket;

public class AudioReceiver extends AsyncTask<Void, Void, Void> {
    private static final int PORT = 5000;
    private static final int SAMPLE_RATE = 44100;
    private static final int BUFFER_SIZE = 1024;

    @Override
    protected Void doInBackground(Void... params) {
        try {
            DatagramSocket socket = new DatagramSocket(PORT);
            byte[] buffer = new byte[BUFFER_SIZE];
            AudioTrack audioTrack = new AudioTrack(AudioManager.STREAM_MUSIC,
                    SAMPLE_RATE, AudioFormat.CHANNEL_OUT_MONO,
                    AudioFormat.ENCODING_PCM_16BIT, BUFFER_SIZE,
                    AudioTrack.MODE_STREAM);

            audioTrack.play();

            while (true) {
                DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
                socket.receive(packet);
                audioTrack.write(packet.getData(), 0, packet.getLength());
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }
}
