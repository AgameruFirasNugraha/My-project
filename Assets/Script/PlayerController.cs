using UnityEngine;
using UnityEngine.InputSystem;

public class PlayerController : MonoBehaviour
{
    [SerializeField] private float walkSpeed = 2.5f;
    [SerializeField] private float sprintSpeed = 4.5f;
    [SerializeField] private float acceleration = 12f;
    [SerializeField] private float turnSpeed = 360f;

    private Rigidbody2D rb;
    private Camera cam;
    private Stamina stamina;
    private Vector2 moveInput;
    private bool sprinting;

    void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
        cam = Camera.main;
        stamina = GetComponent<Stamina>();
    }

    void Update()
    {
        var kb = Keyboard.current;

        moveInput = Vector2.zero;
        if (kb.wKey.isPressed) moveInput += Vector2.up;
        if (kb.sKey.isPressed) moveInput += Vector2.down;
        if (kb.dKey.isPressed) moveInput += Vector2.right;
        if (kb.aKey.isPressed) moveInput += Vector2.left;
        moveInput = moveInput.normalized;

        bool wantsSprint = kb.leftShiftKey.isPressed && moveInput.sqrMagnitude > 0.01f;

        if (stamina != null)
        {
            sprinting = wantsSprint && stamina.CanSprint;
            stamina.Tick(wantsSprint);
        }
        else
        {
            sprinting = wantsSprint;
        }
    }

    void FixedUpdate()
    {
        if (cam == null) { cam = Camera.main; }
        float targetSpeed = sprinting ? sprintSpeed : walkSpeed;
        Vector2 targetVelocity = moveInput * targetSpeed;
        rb.linearVelocity = Vector2.MoveTowards(
            rb.linearVelocity, targetVelocity, acceleration * Time.fixedDeltaTime);

        Vector2 mouseWorld = cam.ScreenToWorldPoint(Mouse.current.position.ReadValue());
        Vector2 dir = mouseWorld - rb.position;
        float targetAngle = Mathf.Atan2(dir.y, dir.x) * Mathf.Rad2Deg;
        float newAngle = Mathf.MoveTowardsAngle(
            rb.rotation, targetAngle, turnSpeed * Time.fixedDeltaTime);
        rb.MoveRotation(newAngle);
    }
}