class CreateLists < ActiveRecord::Migration[5.0]
  def change
    create_table :lists do |t|
      t.references :user, foreign_key: true
      t.references :song, foreign_key: true
      t.string :count 

      t.timestamps
    end
  end
end
