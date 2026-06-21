import os

base_dir = "backend"
pkg = "src/main/java/com/converterhub"

def write_file(path, content):
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# Repositories
write_file(f"{pkg}/repository/UserRepository.java", """
package com.converterhub.repository;

import com.converterhub.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

@Repository
public interface UserRepository extends JpaRepository<User, UUID> {
    Optional<User> findByEmail(String email);
    Optional<User> findByUsername(String username);
    boolean existsByEmail(String email);
    boolean existsByUsername(String username);
}
""")

write_file(f"{pkg}/repository/CategoryRepository.java", """
package com.converterhub.repository;

import com.converterhub.entity.Category;
import org.springframework.data.domain.Sort;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface CategoryRepository extends JpaRepository<Category, UUID> {
    Optional<Category> findBySlug(String slug);
    List<Category> findAllByActiveTrueAndDeletedFalse(Sort sort);
    List<Category> findByDeletedFalse();
}
""")

write_file(f"{pkg}/repository/ConverterRepository.java", """
package com.converterhub.repository;

import com.converterhub.entity.Converter;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface ConverterRepository extends JpaRepository<Converter, UUID> {
    Optional<Converter> findBySlug(String slug);
    Page<Converter> findByCategoryId(UUID categoryId, Pageable pageable);
    Page<Converter> findByNameContainingIgnoreCase(String name, Pageable pageable);
    List<Converter> findTop10ByActiveTrueAndDeletedFalseOrderByConversionCountDesc();
    List<Converter> findByDeletedFalse();
}
""")

write_file(f"{pkg}/repository/FavoriteRepository.java", """
package com.converterhub.repository;

import com.converterhub.entity.Favorite;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

@Repository
public interface FavoriteRepository extends JpaRepository<Favorite, UUID> {
    Page<Favorite> findByUserId(UUID userId, Pageable pageable);
    Optional<Favorite> findByUserIdAndConverterId(UUID userId, UUID converterId);
    boolean existsByUserIdAndConverterId(UUID userId, UUID converterId);
    void deleteByUserIdAndConverterId(UUID userId, UUID converterId);
}
""")

write_file(f"{pkg}/repository/ConversionHistoryRepository.java", """
package com.converterhub.repository;

import com.converterhub.entity.ConversionHistory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface ConversionHistoryRepository extends JpaRepository<ConversionHistory, UUID> {
    Page<ConversionHistory> findByUserIdOrderByCreatedAtDesc(UUID userId, Pageable pageable);
    void deleteByUserIdAndId(UUID userId, UUID id);
    void deleteAllByUserId(UUID userId);
}
""")

write_file(f"{pkg}/repository/AnalyticsRepository.java", """
package com.converterhub.repository;

import com.converterhub.entity.Analytics;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface AnalyticsRepository extends JpaRepository<Analytics, UUID> {
    Optional<Analytics> findByConverterSlugAndDate(String converterSlug, LocalDate date);
    
    @Query("SELECT a FROM Analytics a WHERE a.date = :date ORDER BY a.pageVisits DESC")
    List<Analytics> findTopByDateOrderByPageVisitsDesc(@Param("date") LocalDate date, Pageable pageable);
}
""")

write_file(f"{pkg}/repository/ExchangeRateRepository.java", """
package com.converterhub.repository;

import com.converterhub.entity.ExchangeRate;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface ExchangeRateRepository extends JpaRepository<ExchangeRate, UUID> {
    Optional<ExchangeRate> findByBaseCurrencyAndTargetCurrency(String baseCurrency, String targetCurrency);
    List<ExchangeRate> findAllByBaseCurrency(String baseCurrency);
    void deleteAllByBaseCurrency(String baseCurrency);
}
""")

# DTOs
write_file(f"{pkg}/dto/common/ApiResponse.java", """
package com.converterhub.dto.common;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ApiResponse<T> {
    private boolean success;
    private String message;
    private T data;
    
    @Builder.Default
    private LocalDateTime timestamp = LocalDateTime.now();
    private String path;
}
""")

write_file(f"{pkg}/dto/common/PagedResponse.java", """
package com.converterhub.dto.common;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class PagedResponse<T> {
    private List<T> content;
    private int page;
    private int size;
    private long totalElements;
    private int totalPages;
    private boolean last;
}
""")

write_file(f"{pkg}/dto/auth/LoginRequest.java", """
package com.converterhub.dto.auth;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class LoginRequest {
    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    private String email;

    @NotBlank(message = "Password is required")
    private String password;
}
""")

write_file(f"{pkg}/dto/auth/RegisterRequest.java", """
package com.converterhub.dto.auth;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Data;

@Data
public class RegisterRequest {
    @NotBlank(message = "First name is required")
    @Size(min = 2, max = 50, message = "First name must be between 2 and 50 characters")
    private String firstName;

    @NotBlank(message = "Last name is required")
    @Size(min = 2, max = 50, message = "Last name must be between 2 and 50 characters")
    private String lastName;

    @NotBlank(message = "Username is required")
    @Size(min = 3, max = 30, message = "Username must be between 3 and 30 characters")
    private String username;

    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    private String email;

    @NotBlank(message = "Password is required")
    @Size(min = 8, message = "Password must be at least 8 characters long")
    private String password;
}
""")

write_file(f"{pkg}/dto/auth/AuthResponse.java", """
package com.converterhub.dto.auth;

import com.converterhub.dto.user.UserResponse;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AuthResponse {
    private String accessToken;
    private String refreshToken;
    @Builder.Default
    private String tokenType = "Bearer";
    private long expiresIn;
    private UserResponse user;
}
""")

write_file(f"{pkg}/dto/auth/RefreshTokenRequest.java", """
package com.converterhub.dto.auth;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class RefreshTokenRequest {
    @NotBlank(message = "Refresh token is required")
    private String refreshToken;
}
""")

write_file(f"{pkg}/dto/user/UserResponse.java", """
package com.converterhub.dto.user;

import lombok.Data;
import java.util.UUID;

@Data
public class UserResponse {
    private UUID id;
    private String username;
    private String email;
    private String firstName;
    private String lastName;
    private String role;
}
""")

# We will skip all other DTOs for now and generate them as needed or keep it simple.

print("Repositories and basic DTOs created.")
