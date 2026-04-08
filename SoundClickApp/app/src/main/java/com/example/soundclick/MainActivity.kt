package com.example.soundclick

import android.media.AudioAttributes
import android.media.SoundPool
import android.os.Bundle
import android.os.VibrationEffect
import android.os.Vibrator
import android.os.Build
import android.view.MotionEvent
import android.view.View
import android.widget.ImageView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    private lateinit var soundPool: SoundPool
    private var soundId: Int = 0
    private var soundLoaded: Boolean = false
    private var clickCount: Int = 0

    private lateinit var btnClick: View
    private lateinit var tvCount: TextView
    private lateinit var tvHint: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        btnClick = findViewById(R.id.btnClick)
        tvCount = findViewById(R.id.tvCount)
        tvHint = findViewById(R.id.tvHint)

        // 初始化 SoundPool
        val audioAttributes = AudioAttributes.Builder()
            .setUsage(AudioAttributes.USAGE_GAME)
            .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
            .build()

        soundPool = SoundPool.Builder()
            .setMaxStreams(4)
            .setAudioAttributes(audioAttributes)
            .build()

        soundPool.setOnLoadCompleteListener { _, _, status ->
            if (status == 0) {
                soundLoaded = true
                runOnUiThread {
                    tvHint.text = "点击按钮发出声音！"
                }
            }
        }

        // 加载音频资源
        soundId = soundPool.load(this, R.raw.click_sound, 1)

        // 点击事件
        btnClick.setOnClickListener {
            playSound()
            vibrate()
            clickCount++
            tvCount.text = "已点击：$clickCount 次"
        }

        // 按下/抬起动画效果
        btnClick.setOnTouchListener { v, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
                    v.animate().scaleX(0.92f).scaleY(0.92f).setDuration(80).start()
                }
                MotionEvent.ACTION_UP, MotionEvent.ACTION_CANCEL -> {
                    v.animate().scaleX(1f).scaleY(1f).setDuration(100).start()
                    v.performClick()
                }
            }
            true
        }
    }

    private fun playSound() {
        if (soundLoaded) {
            soundPool.play(soundId, 1f, 1f, 1, 0, 1f)
        }
    }

    private fun vibrate() {
        val vibrator = getSystemService(VIBRATOR_SERVICE) as Vibrator
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            vibrator.vibrate(
                VibrationEffect.createOneShot(30, VibrationEffect.DEFAULT_AMPLITUDE)
            )
        } else {
            @Suppress("DEPRECATION")
            vibrator.vibrate(30)
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        soundPool.release()
    }
}
