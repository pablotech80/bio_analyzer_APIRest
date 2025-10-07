# app/models/biometric_analysis.py
"""
SQLAlchemy model for storing biometric analyses linked to users.

Naming Convention: All fields in English for international consistency.
Spanish translations handled in templates/UI layer.

Principios CoachBodyFit360 aplicados:
- SRP: Solo gestiona persistencia de análisis biométricos
- SoC: Cálculos complejos en services/, modelo solo almacena
- DRY: Método to_dict() reutilizable
- API-First: Listo para consumo desde React/Mobile
- Consistency: All field names in English
"""
from datetime import datetime

from app import db


class BiometricAnalysis(db.Model):
	"""
	Historical biometric analysis snapshot for a user.

	Stores both raw input data and calculated metrics,
	plus FitMaster IA interpretation in consolidated JSON field.

	Bilateral Measurements:
		All muscle circumferences are measured separately for left/right
		to track asymmetries and progression accurately.

	Attributes:
		id: Primary key
		user_id: FK to User (indexed for performance)

		# Input data (required)
		weight: Weight in kg
		height: Height in cm
		age: Age in years
		gender: 'male', 'female', or 'other'
		neck: Neck circumference in cm
		waist: Waist circumference in cm
		hip: Hip circumference in cm (optional for males)

		# 🔥 Bilateral muscle measurements (optional)
		biceps_left: Left biceps circumference in cm
		biceps_right: Right biceps circumference in cm
		thigh_left: Left thigh (quadriceps) circumference in cm
		thigh_right: Right thigh (quadriceps) circumference in cm
		calf_left: Left calf (gemelos) circumference in cm
		calf_right: Right calf (gemelos) circumference in cm

		# Activity data
		activity_factor: Numeric multiplier (1.2 - 1.9)
		activity_level: Categorical level (sedentary, light, moderate, active, very_active)
		goal: User goal (lose_weight, maintain, gain_muscle)

		# Calculated metrics (stored for historical tracking)
		bmi: Body Mass Index
		bmr: Basal Metabolic Rate
		tdee: Total Daily Energy Expenditure
		body_fat_percentage: % body fat
		lean_mass: Lean body mass in kg
		fat_mass: Fat mass in kg
		ffmi: Fat-Free Mass Index
		body_water: Body water percentage
		waist_hip_ratio: WHR metric
		waist_height_ratio: WHtR metric
		metabolic_age: Estimated metabolic age

		# Nutrition targets
		maintenance_calories: Daily calories for maintenance
		protein_grams: Daily protein target
		carbs_grams: Daily carbs target
		fats_grams: Daily fats target

		# 🔥 FitMaster IA consolidated field
		fitmaster_data: JSON with full AI interpretation
			{
				"interpretation": "text analysis...",
				"nutrition_plan": {...},
				"training_plan": {...},
				"generated_at": "ISO timestamp",
				"model_version": "fitmaster-vX.Y"
			}

		# Audit timestamps
		created_at: Record creation timestamp
		updated_at: Last modification timestamp

	Relationships:
		user: Many-to-One with User

	Example:
		>>> analysis = BiometricAnalysis(
		...     user_id=1,
		...     weight=75.5,
		...     height=175,
		...     age=30,
		...     gender='male',
		...     neck=38,
		...     waist=85,
		...     hip=95,
		...     biceps_left=35.2,
		...     biceps_right=35.8,
		...     thigh_left=58.5,
		...     thigh_right=59.0,
		...     calf_left=38.2,
		...     calf_right=38.5
		... )
		>>> db.session.add(analysis)
		>>> db.session.commit()
	"""

	__tablename__ = "biometric_analyses"

	# Primary Key
	id = db.Column(db.Integer, primary_key = True)

	# Foreign Key (indexed for query optimization)
	user_id = db.Column(
		db.Integer,
		db.ForeignKey("users.id", ondelete = "CASCADE"),
		nullable = False,
		index = True
		)

	# ========== INPUT DATA (Required) ==========
	weight = db.Column(db.Float, nullable = False, comment = "Weight in kg")
	height = db.Column(db.Float, nullable = False, comment = "Height in cm")
	age = db.Column(db.Integer, nullable = False, comment = "Age in years")

	gender = db.Column(
		db.String(10),
		nullable = False,
		comment = "Gender: 'male', 'female', or 'other'"
		)

	neck = db.Column(db.Float, nullable = False, comment = "Neck circumference in cm")
	waist = db.Column(db.Float, nullable = False, comment = "Waist circumference in cm")
	hip = db.Column(db.Float, nullable = True, comment = "Hip circumference in cm (optional for males)")

	# ========== 🔥 BILATERAL MUSCLE MEASUREMENTS (Optional) ==========
	# Biceps (bíceps)
	biceps_left = db.Column(
		db.Float,
		nullable = True,
		comment = "Left biceps circumference in cm"
		)
	biceps_right = db.Column(
		db.Float,
		nullable = True,
		comment = "Right biceps circumference in cm"
		)

	# Thighs / Quadriceps (muslos/cuádriceps)
	thigh_left = db.Column(
		db.Float,
		nullable = True,
		comment = "Left thigh (quadriceps) circumference in cm"
		)
	thigh_right = db.Column(
		db.Float,
		nullable = True,
		comment = "Right thigh (quadriceps) circumference in cm"
		)

	# Calves (gemelos/pantorrillas)
	calf_left = db.Column(
		db.Float,
		nullable = True,
		comment = "Left calf circumference in cm"
		)
	calf_right = db.Column(
		db.Float,
		nullable = True,
		comment = "Right calf circumference in cm"
		)

	# ========== ACTIVITY DATA ==========
	activity_factor = db.Column(db.Float, nullable = True, comment = "Activity multiplier (1.2-1.9)")
	activity_level = db.Column(
		db.String(32),
		nullable = True,
		comment = "Activity level: sedentary, light, moderate, active, very_active"
		)
	goal = db.Column(
		db.String(32),
		nullable = True,
		comment = "Goal: lose_weight, maintain, gain_muscle"
		)

	# ========== CALCULATED METRICS ==========
	bmi = db.Column(db.Float, nullable = True, comment = "Body Mass Index")
	bmr = db.Column(db.Float, nullable = True, comment = "Basal Metabolic Rate")
	tdee = db.Column(db.Float, nullable = True, comment = "Total Daily Energy Expenditure")
	body_fat_percentage = db.Column(db.Float, nullable = True, comment = "Body fat %")
	lean_mass = db.Column(db.Float, nullable = True, comment = "Lean body mass in kg")
	fat_mass = db.Column(db.Float, nullable = True, comment = "Fat mass in kg")
	ffmi = db.Column(db.Float, nullable = True, comment = "Fat-Free Mass Index")
	body_water = db.Column(db.Float, nullable = True, comment = "Body water %")
	waist_hip_ratio = db.Column(db.Float, nullable = True, comment = "Waist-to-Hip Ratio")
	waist_height_ratio = db.Column(db.Float, nullable = True, comment = "Waist-to-Height Ratio")
	metabolic_age = db.Column(db.Float, nullable = True, comment = "Estimated metabolic age")

	# ========== NUTRITION TARGETS ==========
	maintenance_calories = db.Column(db.Float, nullable = True, comment = "Daily maintenance calories")
	protein_grams = db.Column(db.Float, nullable = True, comment = "Daily protein target in grams")
	carbs_grams = db.Column(db.Float, nullable = True, comment = "Daily carbs target in grams")
	fats_grams = db.Column(db.Float, nullable = True, comment = "Daily fats target in grams")

	# ========== 🔥 FITMASTER IA DATA (CONSOLIDATED) ==========
	fitmaster_data = db.Column(
		db.JSON,
		nullable = True,
		comment = "Complete FitMaster AI response: interpretation, nutrition, training"
		)

	# ========== AUDIT TIMESTAMPS ==========
	created_at = db.Column(
		db.DateTime,
		default = datetime.utcnow,
		nullable = False,
		comment = "Record creation timestamp"
		)
	updated_at = db.Column(
		db.DateTime,
		default = datetime.utcnow,
		onupdate = datetime.utcnow,
		nullable = False,
		comment = "Last modification timestamp"
		)

	# ========== RELATIONSHIPS ==========
	user = db.relationship(
		"User",
		back_populates = "biometric_analyses"
		)

	def __repr__(self) -> str:
		"""Debug-friendly representation."""
		return (
			f"<BiometricAnalysis id={self.id} user_id={self.user_id} "
			f"created_at={self.created_at.strftime('%Y-%m-%d') if self.created_at else 'N/A'}>"
		)

	# ========== 🆕 CONVENIENCE METHODS ==========

	def to_dict(self, include_fitmaster = True, include_user = False):
		"""
		Serialize analysis to dictionary (API-ready).

		Args:
			include_fitmaster: Whether to include AI data (can be large)
			include_user: Whether to include user basic info

		Returns:
			dict: JSON-serializable representation

		Principle: DRY - Reusable for APIs and templates
		"""
		data = {
			'id': self.id,
			'user_id': self.user_id,
			# Input data
			'weight': self.weight,
			'height': self.height,
			'age': self.age,
			'gender': self.gender,
			'neck': self.neck,
			'waist': self.waist,
			'hip': self.hip,
			# Bilateral muscle measurements
			'biceps_left': self.biceps_left,
			'biceps_right': self.biceps_right,
			'thigh_left': self.thigh_left,
			'thigh_right': self.thigh_right,
			'calf_left': self.calf_left,
			'calf_right': self.calf_right,
			# Activity
			'activity_factor': self.activity_factor,
			'activity_level': self.activity_level,
			'goal': self.goal,
			# Calculated metrics
			'bmi': self.bmi,
			'bmr': self.bmr,
			'tdee': self.tdee,
			'body_fat_percentage': self.body_fat_percentage,
			'lean_mass': self.lean_mass,
			'fat_mass': self.fat_mass,
			'ffmi': self.ffmi,
			'body_water': self.body_water,
			'waist_hip_ratio': self.waist_hip_ratio,
			'waist_height_ratio': self.waist_height_ratio,
			'metabolic_age': self.metabolic_age,
			# Nutrition
			'maintenance_calories': self.maintenance_calories,
			'protein_grams': self.protein_grams,
			'carbs_grams': self.carbs_grams,
			'fats_grams': self.fats_grams,
			# Timestamps
			'created_at': self.created_at.isoformat() if self.created_at else None,
			'updated_at': self.updated_at.isoformat() if self.updated_at else None,
			}

		# Optionally include FitMaster data
		if include_fitmaster and self.fitmaster_data:
			data['fitmaster_data'] = self.fitmaster_data

		# Optionally include user basic info
		if include_user and self.user:
			data['user'] = {
				'id': self.user.id,
				'username': self.user.username,
				'email': self.user.email
				}

		return data

	@property
	def has_fitmaster_analysis(self) -> bool:
		"""
		Check if FitMaster AI has processed this analysis.

		Returns:
			bool: True if fitmaster_data exists and is not empty

		Usage in templates:
			{% if analysis.has_fitmaster_analysis %}
				<a href="...">View AI Plan</a>
			{% endif %}
		"""
		return self.fitmaster_data is not None and bool(self.fitmaster_data)

	@property
	def fitmaster_generated_at(self) -> str | None:
		"""
		Get timestamp when FitMaster analysis was generated.

		Returns:
			str | None: ISO timestamp or None if not available
		"""
		if self.has_fitmaster_analysis:
			return self.fitmaster_data.get('generated_at')
		return None

	@property
	def fitmaster_model_version(self) -> str | None:
		"""
		Get FitMaster model version used for this analysis.

		Returns:
			str | None: Model version or None if not available
		"""
		if self.has_fitmaster_analysis:
			return self.fitmaster_data.get('model_version')
		return None

	# ========== 🔥 BILATERAL ANALYSIS HELPERS ==========

	@property
	def biceps_average(self) -> float | None:
		"""Calculate average biceps circumference from both arms."""
		if self.biceps_left and self.biceps_right:
			return round((self.biceps_left + self.biceps_right) / 2, 2)
		return self.biceps_left or self.biceps_right

	@property
	def biceps_asymmetry(self) -> float | None:
		"""Calculate biceps asymmetry percentage (for tracking imbalances)."""
		if self.biceps_left and self.biceps_right:
			larger = max(self.biceps_left, self.biceps_right)
			smaller = min(self.biceps_left, self.biceps_right)
			return round(((larger - smaller) / larger) * 100, 2)
		return None

	@property
	def thigh_average(self) -> float | None:
		"""Calculate average thigh circumference from both legs."""
		if self.thigh_left and self.thigh_right:
			return round((self.thigh_left + self.thigh_right) / 2, 2)
		return self.thigh_left or self.thigh_right

	@property
	def thigh_asymmetry(self) -> float | None:
		"""Calculate thigh asymmetry percentage (for tracking imbalances)."""
		if self.thigh_left and self.thigh_right:
			larger = max(self.thigh_left, self.thigh_right)
			smaller = min(self.thigh_left, self.thigh_right)
			return round(((larger - smaller) / larger) * 100, 2)
		return None

	@property
	def calf_average(self) -> float | None:
		"""Calculate average calf circumference from both legs."""
		if self.calf_left and self.calf_right:
			return round((self.calf_left + self.calf_right) / 2, 2)
		return self.calf_left or self.calf_right

	@property
	def calf_asymmetry(self) -> float | None:
		"""Calculate calf asymmetry percentage (for tracking imbalances)."""
		if self.calf_left and self.calf_right:
			larger = max(self.calf_left, self.calf_right)
			smaller = min(self.calf_left, self.calf_right)
			return round(((larger - smaller) / larger) * 100, 2)
		return None
