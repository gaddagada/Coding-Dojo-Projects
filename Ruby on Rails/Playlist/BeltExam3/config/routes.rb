Rails.application.routes.draw do

  get '/main' => 'users#index'
  root 'users#index'

  get 'songs' => 'songs#index'
  post 'songs' => 'songs#create'
  get 'songs/:id' => 'songs#show'
  get 'songs/:id/add' => 'songs#add'

  get 'users' => 'users#index'
  post 'users/login' => 'users#login'
  post 'users' => 'users#create'
  get 'users/logout' => 'users#logout'
  get 'users/:id' => 'users#show'
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
