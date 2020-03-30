class SongsController < ApplicationController
    def index
        @all_songs = Song.all.order('created_at DESC')
    end
    
    def show
        @song = Song.find_by(id:params[:id])
        lists = List.where(song:@song)
        @users = User.all
        if(@song == nil)
            redirect_to "/songs"
        end
    end

    def add
        song = Song.find_by(id:params[:id])
        puts song.title
        list = List.where(song:song).find_by_user_id(current_user.id)
        if list.nil?
            l = List.new(song:song,user:current_user, count:1)
            l.save
            song.times_added += 1
            song.save
            if !l.errors.empty?
                flash[:warning] = []
                l.errors.full_messages.each do |msg|
                    flash[:warning].push(msg)
                end
            else
                flash[:success] = ["Song added to playlist!"]
            end
        else
            count = list.count.to_i 
            count += 1
            list.count = count.to_s
            list.save
            song.times_added += 1
            song.save
            flash[:success] = ["Song play count incremented!"]
        end
        redirect_to songs_path
    end

    def create
        song = Song.new(artist:params[:artist], title:params[:title], times_added:0)
        song.save
        if !song.errors.empty?
            flash[:warning] = []
            song.errors.full_messages.each do |msg|
                flash[:warning].push(msg)
            end
        else
            flash[:success] = ["Song Added to Hub!"]
        end
        redirect_to songs_path
    end
end