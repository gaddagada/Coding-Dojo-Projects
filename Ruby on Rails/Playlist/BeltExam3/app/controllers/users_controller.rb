class UsersController < ApplicationController
    def index
        session[:user_id] = nil
    end
    
    def show
        @user = User.find_by(id:params[:id])
        @list = List.where(user_id:params[:id])
        @songs = Song.all
        if(@user == nil)
            redirect_to "/main"
        end
    end

    def create
        user = User.new(user_params)
        user.save
        if !user.errors.empty?
        flash[:warning] = []
            user.errors.full_messages.each do |msg|
                flash[:warning].push(msg)
            end
        redirect_to users_path and return
        else
            flash[:success] = ["User successfully created!"]
            session[:user_id] = user.id
            redirect_to songs_path
        end
    end

    def login
        user = User.find_by_email(params[:email])
        if !user.nil? and user.authenticate(params[:password])
            session[:user_id] = user.id
            flash[:success] = ["Welcome Back #{current_user.first_name}!"]
            redirect_to songs_path
        else
            flash[:warning] = ["Invalid credentials"]
            redirect_to users_path
        end
    end

    def logout
        flash[:success] = ["Successfully logged out!"]
        redirect_to users_path
    end

    private
    def user_params
        params.require(:user).permit(:first_name,:last_name,:email,:password,:password_confirmation)
    end
end
