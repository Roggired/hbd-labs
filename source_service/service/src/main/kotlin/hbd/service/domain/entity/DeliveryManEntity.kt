package hbd.service.domain.entity

import hbd.service.domain.model.DeliveryMan
import jakarta.persistence.Entity
import jakarta.persistence.GeneratedValue
import jakarta.persistence.GenerationType
import jakarta.persistence.Id
import java.util.UUID

@Entity(name = "delivery_man")
class DeliveryManEntity (
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    val id: UUID,
    val name: String
)

fun DeliveryManEntity.toModel(): DeliveryMan =
    DeliveryMan(
        id = id,
        name = name
    )