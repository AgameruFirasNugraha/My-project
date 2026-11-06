using UnityEngine;
using UnityEngine.UI;

public class HeartPulse : MonoBehaviour
{
    [SerializeField] private Image heartImage;
    [SerializeField] private Sprite restFrame;
    [SerializeField] private Sprite beatFrame;
    [SerializeField] private float beatTime = 0.12f;
    [SerializeField] private float gapTime = 0.1f;
    [SerializeField] private float restTime = 0.8f;

    private float timer;

    void Update()
    {
        timer = timer + Time.deltaTime;

        float cycle = beatTime + gapTime + beatTime + restTime;
        if (timer >= cycle)
        {
            timer = timer % cycle;
        }

        bool firstBeat = timer < beatTime;
        bool secondBeat = timer >= beatTime + gapTime && timer < beatTime + gapTime + beatTime;

        if (firstBeat || secondBeat)
        {
            heartImage.sprite = beatFrame;
        }
        else
        {
            heartImage.sprite = restFrame;
        }
    }
}
