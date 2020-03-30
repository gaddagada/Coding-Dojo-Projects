class Song < ApplicationRecord
    has_many :lists

	validates :artist,:title, presence: true, length: { in: 8..20 }
end
