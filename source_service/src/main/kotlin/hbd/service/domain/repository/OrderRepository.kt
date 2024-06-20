package hbd.service.domain.repository

import hbd.service.domain.entity.OrderEntity
import org.springframework.data.domain.Page
import org.springframework.data.domain.Pageable
import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.data.jpa.repository.Query
import java.time.LocalDateTime
import java.util.*

interface OrderRepository: JpaRepository<OrderEntity, UUID> {
    @Query(
        """
            SELECT o FROM OrderEntity o
            WHERE o.orderDateCreated > :deliveryTimeFilterClause
        """
    )
    fun findAllFiltered(
        deliveryTimeFilterClause: LocalDateTime,
        pageable: Pageable
    ): Page<OrderEntity>
}
