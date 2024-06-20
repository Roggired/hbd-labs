package hbd.service.domain.repository

import hbd.service.domain.entity.DeliveryEntity
import org.springframework.data.domain.Page
import org.springframework.data.domain.Pageable
import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.data.jpa.repository.Query
import java.time.LocalDateTime
import java.util.*

interface OrderRepository: JpaRepository<DeliveryEntity, UUID> {
    @Query(
        """
            SELECT o FROM DeliveryEntity o
            WHERE o.orderDateCreated > :deliveryTimeFilterClause
        """
    )
    fun findAllFiltered(
        deliveryTimeFilterClause: LocalDateTime,
        pageable: Pageable
    ): Page<DeliveryEntity>
}
