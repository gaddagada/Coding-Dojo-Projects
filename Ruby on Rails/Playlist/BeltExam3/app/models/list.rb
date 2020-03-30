class List < ApplicationRecord
  belongs_to :user
  belongs_to :song
  has_many :songs
  has_many :users

  validates :user_id,:song_id, presence: true
end
