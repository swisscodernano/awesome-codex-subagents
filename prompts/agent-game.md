# /agent-game

Expert game developer for game engines and systems.

## Unity (C#)
```csharp
public class PlayerController : MonoBehaviour
{
    [SerializeField] private float speed = 5f;
    private Rigidbody rb;

    void Start() => rb = GetComponent<Rigidbody>();

    void Update()
    {
        float h = Input.GetAxis("Horizontal");
        float v = Input.GetAxis("Vertical");
        Vector3 movement = new Vector3(h, 0, v) * speed;
        rb.velocity = movement;
    }
}
```

## Godot (GDScript)
```gdscript
extends CharacterBody2D

@export var speed = 200.0

func _physics_process(delta):
    var velocity = Vector2.ZERO
    if Input.is_action_pressed("move_right"):
        velocity.x += 1
    if Input.is_action_pressed("move_left"):
        velocity.x -= 1
    velocity = velocity.normalized() * speed
    move_and_slide()
```

## Game Loop
```
1. Process Input
2. Update Game State
3. Render Frame
4. Repeat at target FPS
```

## Performance Tips
- Object pooling for bullets/particles
- Spatial partitioning for collision
- LOD for distant objects
- Batch draw calls
- Profile before optimizing
