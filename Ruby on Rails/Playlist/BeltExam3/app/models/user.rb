class User < ApplicationRecord
  has_secure_password
  
  EMAIL_REGEX = /\A([^@\s]+)@((?:[-a-z0-9]+\.)+[a-z]+)\z/i
  has_many :lists

  validates :first_name, :last_name,:email, presence: true, length: { in: 2..20 }
  validates :password,confirmation: true, length: { in: 8..20 }, on: :create
  validates :email, uniqueness: { case_sensitive: false }, format: {with: EMAIL_REGEX}
end
